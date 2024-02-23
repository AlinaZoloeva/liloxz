import re

import pdfplumber


def extract_table(pdf_path, page_num, table_num):
    pdf = pdfplumber.open(pdf_path)
    table_page = pdf.pages[page_num]
    table = table_page.extract_tables()[table_num]
    return table

def table_converter(table):
    table_string = [[],[],[],[],[],[]]
    for row_num in range(len(table)):
        row = table[row_num]
        cleaned_row = [item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item for item in row]
        table_string[row_num // 5].append(cleaned_row)

    return table_string


def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

t = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
for i in range(1, 11, 2):
    print(t[i])



