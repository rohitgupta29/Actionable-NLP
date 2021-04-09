import os
from PyPDF2 import PdfFileWriter, PdfFileReader
from pdfminer.pdfpage import PDFPage
from pdfminer.high_level import extract_pages

module_path = os.path.dirname(os.path.realpath("__file__"))
input_path = os.path.join(module_path, 'scanned_even.pdf') #input file


def no_of_pages(filename):
    total_pages = len(list(extract_pages("scanned_even.pdf")))
    return total_pages



def modify_even_page_pdf():
    infile = input_path
    outfile = "Output_new1.pdf"

    page_range = "1-2,6"

    output = PdfFileWriter()
    input_pdf = PdfFileReader(open(infile, "rb"))
    output_file = open(outfile, "wb")


    page_ranges = (x.split("-") for x in page_range.split(","))
    range_list = [i for r in page_ranges for i in range(int(r[0]), int(r[-1]) + 1)]


    for p in range_list:
        # Subtract 1 to deal with 0 index
        output.addPage(input_pdf.getPage(p - 1))
    output.write(output_file)
    return outfile



def get_pdf_searchable_pages(filename= "scanned_even.pdf"):
    """Checks pdf for searchable and non searchable pages
    to check if the pdf is digital or scanned or a mix of both """
    
    searchable_pages = []
    non_searchable_pages = []
    page_num = 0
    with open(filename, 'rb') as infile:
      total_pages = len(list(extract_pages(filename)))
      print(f"Total Pages are {total_pages}")
      
      

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
    if no_of_pages("scanned_even.pdf") % 2 != 0:
      return get_pdf_searchable_pages("scanned_even.pdf")
    else:
      return get_pdf_searchable_pages(modify_even_page_pdf())
    


if __name__ == '__main__':
   main()
    

