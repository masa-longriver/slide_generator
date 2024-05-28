import glob
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import fitz
from pylatex import Document, Section, Command
from pylatex.utils import NoEscape


def read_tex_file(tex_path: str) -> dict:
    """
    指定されたディレクトリ内のすべての.texファイルを読み込み、
    その内容を辞書として返します。
    キーは拡張子を除いたファイル名で、値はファイルの内容です。

    Args:
        tex_path (str): .texファイルを含むディレクトリのパス。

    Returns:
        dict: ファイル名をキー、ファイル内容を値とする辞書。
    """
    tex_contents = {}
    tex_files = glob.glob(os.path.join(tex_path, "*.tex"))
    for tex_file in tex_files:
        with open(tex_file, 'r', encoding='utf-8') as file:
            content = file.read()
            section_title = os.path.basename(tex_file).replace('.tex', '')
            tex_contents[section_title] = content
    
    return tex_contents

def create_slide_from_tex(tex_contents: dict, paper_title: str) -> Document:
    """
    .texファイルの内容からスライドを作成する関数。

    Args:
        tex_contents (dict): セクションタイトルをキー、内容を値とする辞書。
        paper_title (str): スライドのタイトル。

    Returns:
        Document: LaTeXのドキュメントオブジェクト。
    """
    doc = Document(documentclass='beamer')
    doc.preamble.append(Command('title', paper_title))
    doc.append(NoEscape(r'\maketitle'))

    for section_title, content in tex_contents.items():
        with doc.create(Section(section_title)):
            doc.append(NoEscape(content))
    
    return doc

def generate_slide(paper_title: str) -> None:
    """
    指定された論文タイトルに基づいてスライドを生成し、PDFとして保存します。

    Args:
        paper_title (str): スライドのタイトルとなる論文タイトル。
    """
    tex_path = os.path.join("../logs/texs", paper_title)
    tex_contents = read_tex_file(tex_path)

    doc = create_slide_from_tex(tex_contents, paper_title)
    pdf_path = os.path.join("../logs/pdfs", f"{paper_title}.pdf")
    doc.generate_pdf(pdf_path, clean_tex=False)
            
