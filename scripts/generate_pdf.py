import glob
import os
import subprocess
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
import fitz
from openai import OpenAI
from pylatex import Document, Section, Command
from pylatex.utils import NoEscape

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI()


def read_tex_file(tex_path: str) -> str:
    """
    指定されたディレクトリ内のすべての.texファイルを読み込み、
    結合された.texファイルの内容を返します。

    Args:
        tex_path (str): .texファイルを含むディレクトリのパス。

    Returns:
        str: 結合された.texファイルの内容。
    """
    tex_files = sorted(glob.glob(os.path.join(tex_path, "*.tex")))

    if not tex_files:
        return ""

    # 最初のファイルをヘッダーとフッターの定義に使用
    with open(tex_files[0], 'r', encoding='utf-8') as first_file:
        first_content = first_file.read()
        header_end = first_content.find(r'\begin{document}')
        header = first_content[:header_end] + r'\begin{document}'
        footer_start = first_content.rfind(r'\end{document}')
        footer = r'\end{CJK}' + first_content[footer_start:]

    # 残りのファイルを本文として結合
    body = ""
    for tex_file in tex_files:
        with open(tex_file, 'r', encoding='utf-8') as file:
            content = file.read()
            # \documentclass と \begin{document} の宣言を除去
            content = content.replace(r"\documentclass{beamer}", "")
            content = content.replace(r"\begin{document}", "")
            content = content.replace(r"\end{document}", "")
            body += content + "\n"
    
    # 結合されたコンテンツを作成
    combined_content = header + body + footer

    return combined_content

def create_slide_from_tex(combined_tex_content: str, paper_title: str) -> Document:
    """
    結合された.texファイルの内容からスライドを作成する関数。

    Args:
        combined_tex_content (str): 結合された.texファイルの内容。
        paper_title (str): スライドのタイトル。

    Returns:
        Document: LaTeXのドキュメントオブジェクト。
    """
    # ドキュメントを作成
    doc = Document(documentclass='beamer')
    doc.packages.append(NoEscape(r'\usepackage[utf8]{inputenc}'))  # UTF-8エンコーディングを使用
    doc.packages.append(NoEscape(r'\usepackage{xeCJK}'))  # XeLaTeX用のCJKパッケージ
    doc.packages.append(NoEscape(r'\setCJKmainfont{IPAexMincho}'))  # CJKフォントを設定
    doc.preamble.append(Command('title', paper_title))
    
    # 全体の内容を追加
    doc.append(NoEscape(combined_tex_content))
    
    return doc

# def modify_tex(tex_path: str) -> None:
#     """
#     指定されたTEXファイルを読み込み、LaTeXのルールに従って修正します。

#     Args:
#         tex_path (str): 修正するTEXファイルのパス。
#     """
#     with open(tex_path, 'r', encoding='utf-8') as tex_file:
#         tex_content = tex_file.read()
    
#     system_prompt = f"""
#     あなたはLaTeXのベテランエンジニアです。
#     不正確なLaTeXコードを修正する完璧な仕事をこなします。
#     """
#     user_prompt = f"""
#     {tex_content}

#     上記のLaTeXから、スライドを生成したいと考えていますが、LaTeXの記述が不正確です。
#     上記のLaTeXファイルの中身を、LaTeXのルールに従って修正してください。
#     出力したLaTeXコードは、そのまま使用するため安全に生成してください。
#     出力はLaTeXコードのみを出力、その他には何も書かないでください。
#     """
#     response = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {
#                 "role": "user",
#                 "content": user_prompt
#             }
#         ]
#     )
#     modified_tex_content = response.choices[0].message.content
#     modified_tex_content = modified_tex_content.replace("```latex", "").replace("```", "").strip()
#     with open(tex_path, 'w', encoding='utf-8') as tex_file:
#         tex_file.write(modified_tex_content)

def generate_slide(paper_title: str) -> None:
    """
    指定された論文タイトルに基づいてスライドを生成し、PDFとして保存します。

    Args:
        paper_title (str): スライドのタイトルとなる論文タイトル。
    """
    tex_path = os.path.join("../logs/texs", paper_title)
    tex_contents = read_tex_file(tex_path)

    doc = create_slide_from_tex(tex_contents, paper_title)
    tex_path = os.path.join("../logs/texs", f"{paper_title}")
    doc.generate_tex(tex_path)
    tex_path2 = f"../texs/{paper_title}.tex"
    output_dir="../logs/pdfs"
    subprocess.run(
        ["xelatex", '--interaction=nonstopmode', tex_path2],
        check=True,
        cwd=output_dir
    )

