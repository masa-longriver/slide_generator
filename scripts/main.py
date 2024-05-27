import argparse
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

parser = argparse.ArgumentParser()
parser.add_argument('--paper', type=str, required=True)

from scripts.extrace_yaml import read_pdf, generate_yaml, save_text, save_yaml
from scripts.generate_tex import extract_yaml_structure, generate_tex

if __name__ == "__main__":
    args = parser.parse_args()

    for dir_nm in ["pdfs", "texs", "texts", "yamls"]:
        os.makedirs(f"../logs/{dir_nm}", exist_ok=True)

    # pdf_content = read_pdf(f"../resources/{args.paper}.pdf")
    # print("📖 1. PDFの読み込みが完了しました！")

    # save_text(pdf_content, f"../logs/texts/{args.paper}.txt")
    # print("💾 2. PDFの保存が完了しました！")

    # yaml_content = generate_yaml(pdf_content)
    # print("📝 3. YAMLの生成が完了しました！")

    # save_yaml(yaml_content, f"../logs/yamls/{args.paper}.yaml")
    # print("💾 4. YAMLの保存が完了しました！")

    # result = extract_yaml_structure(f"../logs/yamls/{args.paper}.yaml")
    # print("🗂️ 5. YAMLの構成を取り出しました！")

    # generate_tex(result, args.paper)
    # print("📝 6. LaTeXファイルの生成が完了しました！")
