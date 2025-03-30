import pdfplumber
import re
from io import BytesIO

def extract_code_with_context(pdf_path):
    extracted_code = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if not text:
                continue

            lines = text.split("\n")
            for i, line in enumerate(lines):
                if re.match(r"^\s{4,}|\t|[{}()\[\]=<>]", line):
                    before_context = " ".join(lines[i - 1].split()[-3:]) if i > 0 else ""
                    after_context = " ".join(lines[i + 1].split()[:3]) if i < len(lines) - 1 else ""
                    extracted_code.append(f"**Before:** {before_context}\n```code\n{line.strip()}\n```\n**After:** {after_context}")

    if not extracted_code:
        # Auto-generate a placeholder code block
        extracted_code.append("## Example Code Block\n```python\ndef placeholder():\n    print('This is a placeholder.')\n```\n")

    return "\n\n".join(extracted_code)


# Temporary Test Function
if __name__ == "__main__":
    pdf_path = "q-pdf-to-markdown.pdf"  # Change this path if needed
    output = extract_code_with_context(pdf_path)
    print(output)
