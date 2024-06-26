import os
import pickle
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
from openai import OpenAI
import yaml

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI()


def extract_yaml_structure(yaml_file_path: str) -> list:
    """
    指定されたYAMLファイルの構造を抽出し、論文タイトル、章、節、項の情報をリストとして返します。

    Args:
        yaml_file_path (str): YAMLファイルのパス

    Returns:
        list: 論文タイトル、章、節、項が順番通りに格納されたリスト
    """
    with open(yaml_file_path, 'r', encoding='utf-8') as file:
        yaml_content = yaml.safe_load(file)

    user_prompt = f"""
    yaml:
    {yaml_content}

    上記のYAMLファイルの中身から、
    以下のPythonコードを生成してください。

    # YAMLファイルの中身から「論文タイトル」「章」「節」「項」の構成を読み込み、それらを順番通りに取り出す。
    # YAMLファイルは読み込まず、中身はPythonファイルの中に書き込む（その際、バックスラッシュは決して入れない）。
    # 各要素が論文タイトル、章、節、項かどうかを判定し、安全に処理します。
    # return: 論文タイトル、章、節、項が順番通りに格納されたリスト
    # コードかYAMLファイルの中身を見ながら慎重に組んでください。
    # リストには、文字列で"（インデックス、タイトル、中身）"の形で格納してください。
    # 結果を格納するリストを初期化
    # YAMLファイルの内容を順番に処理するループ
    # 章のキーが'章'で始まるかチェック
    # 章のタイトルをリストに追加
    # 節が存在するかチェック
    # 節の内容を処理するループ
    # 節のキーが'節'で始まるかチェック
    # 節のタイトルをリストに追加
    # 項が存在するかチェック
    # 項の内容を処理するループ
    # 項のキーが'項'で始まるかチェック
    # 項のタイトルをリストに追加
    # '内容'キーがない場合は空文字を返す
    # 処理結果（リスト）をresult変数に代入

    pythonのコードブロックのみを出力、その他説明は何も書かないでください。
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": f"{user_prompt}"
            }
        ]
    )
    code = response.choices[0].message.content
    code = code.replace("```python", "").replace("```", "").strip()
    with open("gen_pyfiles/extract_yaml_structure.py", "w") as f:
        f.write(code)
    global_context = {}
    local_context = {}
    exec(code, global_context, local_context)

    return local_context['result']

def save_result(result: list, paper_title: str) -> None:
    """
    結果をpickleファイルに保存する関数。

    :param result: 保存する結果のリスト
    :param paper_title: 論文のタイトル
    """
    with open(f"../logs/middle_results/{paper_title}.pkl", "wb") as f:
        pickle.dump(result, f)

def generate_tex(paper_title: str) -> None:
    """
    指定されたYAML構造に基づいて、LaTeXファイルを生成する関数。

    :param yaml_structure: 論文タイトル、章、節、項が順番通りに格納されたリスト
    """
    with open(f"../logs/middle_results/{paper_title}.pkl", "rb") as f:
        yaml_structure = pickle.load(f)
    save_dir = os.path.join("../logs/texs", paper_title)
    os.makedirs(save_dir, exist_ok=True)

    for i, content in enumerate(yaml_structure):
        system_prompt = """
        あなたは日本の学術研究のスペシャリストで、大学教授です。
        これから勉強会で、与えられた論文について、
        情報学を専攻している大学院生に説明します。
        勉強会の準備として、論文を説明するためのスライドをLaTeXで作成します。
        """

        if i == 0:
            add_cond = "# \end{document}は書かないでください。"
        elif i > 0 and i < len(yaml_structure) - 1:
            add_cond = "# コマンドは\begin{frame}, \end{frame}, \begin{itemize}, \end{itemize}, \item以外は絶対に使用しないでください。"
            add_cond += "# \fontfamily, \\usefont, \renewcommand, \setmainfont は書かないでください。"
        else:
            add_cond = "# 最後に\end{document}を書いてください。"

        user_prompt = f"""
        content:
        {content}

        上記の内容から内容を膨らませて、
        学生に説明するためのスライドをLaTeXで生成してください。
        これは{len(yaml_structure)}つのスライドのうち、{i+1}番目のスライドです。

        # 生成したLaTeXコードはスライドPDFの生成に使用します。
        # そのままPDFの生成に使用できるよう、コードは正しい位置に出力してください。
        # 説明はすべて日本語で出力してください。
        # フォントには'IPAexMincho'を使用してください。
        
        {add_cond}
        LaTeXコードのみを出力、その他には何も書かないでください。
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )
        tex_content = response.choices[0].message.content
        tex_content = tex_content.replace("```latex", "").replace("```", "").strip()
        with open(f"{save_dir}/number_{i:02}.tex", "w") as f:
            f.write(tex_content)
        print(f"({i+1}/{len(yaml_structure)}) texファイル生成完了！")
