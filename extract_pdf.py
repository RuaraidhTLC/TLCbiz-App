import PyPDF2

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        num_pages = len(pdf_reader.pages)
        print(f"Total number of pages: {num_pages}")
        
        for page_num in range(num_pages):
            page = pdf_reader.pages[page_num]
            text += f"\n\n--- Page {page_num + 1} ---\n\n"
            text += page.extract_text()
    
    return text

if __name__ == "__main__":
    pdf_path = "servicem8_guidelines.pdf"
    text = extract_text_from_pdf(pdf_path)
    
    # Print a summary of the text
    print("\n\nPDF Content Summary:")
    print(text[:2000] + "..." if len(text) > 2000 else text)
    
    # Save the complete text to a file
    with open("servicem8_guidelines.txt", "w", encoding="utf-8") as f:
        f.write(text)
    
    print("\nFull text saved to servicem8_guidelines.txt")