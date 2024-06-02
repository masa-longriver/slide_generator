import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dotenv import load_dotenv
import fitz
from openai import OpenAI
import yaml

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
client = OpenAI()


def read_pdf(pdf_path: str) -> str:
    """
    指定されたPDFファイルからテキストを抽出する関数。

    :param pdf_path: PDFファイルのパス
    :return: 抽出されたテキストを含む文字列
    """
    # PDFファイルを開く
    document = fitz.open(pdf_path)
    text = ""

    # 全ページのテキストを抽出
    for page_num in range(document.page_count):
        page = document.load_page(page_num)
        text += page.get_text()

    return text

def save_text(text_content: str, output_file_path: str) -> None:
    """
    テキスト文字列を指定されたファイルに保存する関数。

    :param text_content: 保存するテキスト内容
    :param output_file_path: 保存先のファイルパス
    """
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(text_content)
    print(f"テキストファイルが正常に保存されました: {output_file_path}")


def generate_yaml(paper_content: str) -> str:
    """
    OpenAIのAPIを使用して、与えられた論文の中身を章や内容ごとに階層分けした
    yamlファイルを出力する関数。

    :param paper_content: 論文の内容を含む文字列
    :return: 階層分けされた内容を含むyaml文字列
    """
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": """
                あなたは学術研究のスペシャリストで、大学教員です。
                これから勉強会で、とある論文について学生に説明します。
                """
            },
            {
                "role": "user",
                "content": f"""
                {paper_content}
                上記の論文内容をyaml形式に変換してください。
                - 構成は「章」「節」「項」という階層で出力してください。
                - 内容は抜け漏れが無いように、箇条書きで出力してください。
                - Abstractも含めて出力してください。
                - 日本語で回答してください。
                - yaml以外の出力はしないでください。
                """
            }
        ]
    )
    yaml_content = response.choices[0].message.content
    yaml_content = yaml_content.replace("```yaml", "").replace("```", "")
    
    return yaml_content

def save_yaml(yaml_content: str, output_file_path: str) -> None:
    """
    yaml文字列を指定されたファイルに保存する関数。

    :param yaml_content: yaml形式の文字列
    :param output_file_path: 保存先のファイルパス
    """
    with open(output_file_path, 'w', encoding='utf-8') as file:
        file.write(yaml_content)
    print(f"YAMLファイルが正常に保存されました: {output_file_path}")