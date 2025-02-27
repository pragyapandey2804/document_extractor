import fitz  # PyMuPDF for text extraction
import pdfplumber  # For table extraction
import json

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF and returns structured data"""
    doc = fitz.open(pdf_path)
    text_data = {}

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        
        lines = text.strip().split("\n")
        if lines:
            heading = lines[0].strip()
            content = "\n".join(lines[1:]).strip()
            text_data[heading] = content

    return text_data

def extract_tables_from_pdf(pdf_path):
    """Extracts tables from a PDF and returns them as a list of dictionaries"""
    table_data = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if table:
                    headers = table[0]  # First row as headers
                    for row in table[1:]:
                        table_data.append(dict(zip(headers, row)))

    return table_data

if __name__ == "__main__":
    # Ask the user for the PDF file path
    pdf_path = input("Enter the full path to the PDF file: ").strip()
    
    try:
        # Extract text and tables
        text_data = extract_text_from_pdf(pdf_path)
        table_data = extract_tables_from_pdf(pdf_path)

        # Combine results into JSON
        final_data = {
            "Headers": text_data,
            "List_items": table_data
        }

        # Save JSON file
        json_file = "extracted_data.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(final_data, f, indent=4, ensure_ascii=False)

        print(f"Data saved to {json_file}")
        print(json.dumps(final_data, indent=4, ensure_ascii=False))  # Display JSON output
    except Exception as e:
        print(f"Error: {e}")