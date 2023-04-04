from PyPDF2 import PdfReader
import fitz
import pandas as pd

reader = PdfReader('rettsyndrome.pdf')

doc = fitz.open('rettsyndrome.pdf')
count = doc.page_count
textList = []
#print(doc[1].get_text())
with open('rett.txt', 'w') as f:
    x = ''
    f.write(x)

