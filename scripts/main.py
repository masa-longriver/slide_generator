import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.extrace_yaml import read_pdf, generate_yaml, save_yaml

if __name__ == "__main__":
    pdf_content = read_pdf("../resources/timesfm.pdf")
    yaml_content = generate_yaml(pdf_content)
    save_yaml(yaml_content, "../logs/yamls/timesfm.yaml")