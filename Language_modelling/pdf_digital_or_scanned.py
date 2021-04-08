# Function to check whether a pdf is digital or scanned or a mixture of both. 


from pdfminer.pdfpage import PDFPage
import os

module_path = os.path.dirname(os.path.realpath("__file__"))
input_path = os.path.join(module_path, 'scanned_pdf.pdf') #input file


def get_pdf_searchable_pages(filename):
    """Checks pdf for searchable and non searchable pages
    to check if the pdf is digital or scanned or a mix of both """
    
    searchable_pages = []
    non_searchable_pages = []
    page_num = 0
    with open(filename, 'rb') as infile:

        for page in PDFPage.get_pages(infile):
            page_num += 1
            if 'Font' in page.resources.keys():
                searchable_pages.append(page_num)
            else:
                non_searchable_pages.append(page_num)
    if page_num > 0:
        if len(searchable_pages) == 0:
            print(f"Document '{filename}' has {page_num} page(s). "
                  f"Complete document is non-searchable")
        elif len(non_searchable_pages) == 0:
            print(f"Document '{filename}' has {page_num} page(s). "
                  f"Complete document is searchable")
        else:
            print(f"searchable_pages : {searchable_pages}")
            print(f"non_searchable_pages : {non_searchable_pages}")
    else:
        print(f"Not a valid document")

def main():
    get_pdf_searchable_pages(input_path)
    get_pdf_searchable_pages("scanned_pdf.pdf")


if __name__ == '__main__':
   main()
