import pdfplumber

def scanned_or_text_pdf(filename):
  """If text = None, file is Scanned"""
  with pdfplumber.open(filename) as pdf:
    page = pdf.pages[0]
    text = page.extract_text()
    print(text)
    if text:
        print("This PDF is not Scanned")
    else:
        print("This PDF is fully Scanned")

scanned_or_text_pdf("scanned_image.pdf")
