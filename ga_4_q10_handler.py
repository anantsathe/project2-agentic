import pdfplumber
import subprocess
import tempfile
from fastapi import UploadFile
from io import BytesIO

def extract_text_and_links(pdf_file: BytesIO):
    """
    Extracts text and links from the given PDF file.
    """
    extracted_text = []
    extracted_links = []

    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)

            # Extract links (annotations)
            if "annots" in page.to_dict():
                for annot in page.to_dict()["annots"]:
                    if annot.get("uri"):
                        url = annot.get("uri")
                        extracted_links.append(f"[{url}]({url})")

    return "\n\n".join(extracted_text), "\n\n".join(extracted_links)

def solve_ga_4_q10(file: UploadFile) -> dict:
    try:
        # Load the PDF file
        pdf_data = file.file.read()
        pdf_file = BytesIO(pdf_data)
        
        # Extract text and links
        markdown_content, markdown_links = extract_text_and_links(pdf_file)

        if not markdown_content.strip():
            return {"answer": "Error: Could not extract text from the PDF."}

        # Append links at the end
        markdown_final = markdown_content.replace("\\n", "\n")  # Ensure real line breaks
        if markdown_links:
            markdown_final += "\n\n" + markdown_links

        # Save extracted content to a temporary Markdown file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as temp_md:
            temp_md.write(markdown_final.encode("utf-8"))
            temp_md_path = temp_md.name
        
        # Format using Prettier (ensure Prettier 3.4.2 is installed)
        try:
            result = subprocess.run(
                ["prettier", "--parser", "markdown", "--write", temp_md_path], 
                capture_output=True, 
                text=True
            )
            if result.returncode != 0:
                return {"answer": f"Prettier formatting failed: {result.stderr}"}
        except subprocess.CalledProcessError:
            return {"answer": "Error: Prettier formatting failed. Ensure Prettier 3.4.2 is installed."}
        
        # Read formatted Markdown
        with open(temp_md_path, "r", encoding="utf-8") as f:
            formatted_markdown = f.read()
        
        return {"answer": formatted_markdown}
    
    except Exception as e:
        return {"answer": f"Error: {str(e)}"}
