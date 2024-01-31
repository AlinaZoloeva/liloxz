import requests
from bs4 import BeautifulSoup
import csv

def scrape_page(soup, quotes):
    quote_elements = soup.find_all('div', class_='quote')

    for quote_element in quote_elements:
        text = quote_element.find('span', class_='text').text
        author = quote_element.find('small', class_='author').text

        tag_elements = quote_element.find('div', class_='tags').find_all('a', class_='tag')

        tags = []
        for tag_element in tag_elements:
            tags.append(tag_element.text)

        quotes.append(
            {
                'text': text,
                'author': author,
                'tags': ', '.join(tags)
            }
        )

base_url = 'https://quotes.toscrape.com'



page = requests.get(base_url)

soup = BeautifulSoup(page.text, 'html.parser')

quotes = []

scrape_page(soup, quotes)

next_li_element = soup.find('li', class_='next')

while next_li_element is not None:
    next_page_relative_url = next_li_element.find('a', href=True)['href']

    page = requests.get(base_url + next_page_relative_url)

    soup = BeautifulSoup(page.text, 'html.parser')

    scrape_page(soup, quotes)

    next_li_element = soup.find('li', class_='next')

with open('quotes.csv', 'w', encoding='utf-8', newline='') as csv_file:
    writer = csv.writer(csv_file, delimiter=',')
    writer.writerow(['Text', 'Author', 'Tags'])
    for quote in quotes:
        writer.writerow(quote.values())



csv_file.close()


