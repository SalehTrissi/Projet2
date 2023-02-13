import csv
import math
from pprint import pprint

import requests
from bs4 import BeautifulSoup

import constants


def parse_html(url: str):
    """ Retourne le contenu de la page html """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    return soup


def get_data_of_one_book(url: str):
    response = parse_html(url)
    table_all_td = response.find('table', {'class': 'table table-striped'}).find_all('td')
    product_page_url = url
    title = response.find('head').title.text.strip()
    universal_product_code = table_all_td[0].text
    price_including_tax = table_all_td[3].text
    price_excluding_tax = table_all_td[2].text
    number_available = table_all_td[5].text
    review_rating = response.find("p", class_="star-rating")["class"][1]
    try:
        product_description = response.find('div', {'id': 'product_description'}).find_next_sibling().text
    except:
        product_description = " "
    category = response.find('ul', {'class': 'breadcrumb'}).find_all('li')[
                    2].text.strip()
    image_url = f'{constants.url}/' + response.find("img")["src"].lstrip('./')

    return product_page_url, universal_product_code, title, price_including_tax, price_excluding_tax, \
        number_available, product_description, category, review_rating, image_url


def get_data_of_all_books(category_url: str):
    books_urls = get_url_book_from_category(category_url)
    books_data = []
    for book_url in books_urls:
        book_data = get_data_of_one_book(book_url)
        books_data.append(book_data)
        print(book_data)
    return books_data


def get_number_of_pages(category_url: str):
    """
    On récupère le nombre total des livres de la catégorie, on divise ce nombre par 20 le number de livre dans le page
    et on arrondit au nombre supérieur pour récupérer le number de pages.
    :param category_url:
    :return: Numéro les pages présentes dans la catégorie
    """
    response = parse_html(category_url)
    number_books_in_category = response.find('form', {'class': 'form-horizontal'}).find('strong').text
    number_of_pages = math.ceil(int(number_books_in_category) / 20)
    return number_of_pages


def get_pages_urls(category_url: str):
    """ Recuperation toutes les urls des pages de chaque categories """
    number_of_pages = get_number_of_pages(category_url)
    pages_urls = []
    if number_of_pages == 1:
        return [category_url]
    else:
        for i in range(number_of_pages):
            page_url = category_url.replace("index", f"page-{i + 1}")
            pages_urls.append(page_url)
    return pages_urls


def get_url_book_from_category(category_url: str):
    """
    Recuperation toutes les livres dans un category
    :param category_url:
    :return: urls_book (tous les liens des livres)
    """
    urls_books = []
    for page_url in get_pages_urls(category_url):
        response = parse_html(page_url)
        link_book = response.find('ol', {'class': 'row'}) \
            .find_all('li', {'class': 'col-xs-6 col-sm-4 col-md-3 col-lg-3'})
        for links in link_book:
            url_book = f"{constants.url}/catalogue/" + links.find('h3').a['href'].strip('./')
            urls_books.append(url_book)
    return urls_books


def get_all_categories_url_and_names():
    """
    Récupère tous les liens et les nomes de toutes les catégories
    :return:
    """
    response = parse_html(constants.url)
    all_categories_urls = []
    all_categories_names = []
    links = response.find('ul', {'class': 'nav nav-list'}).find('ul').find_all('li')
    for link_categories in links:
        all_categories_names.append(link_categories.text.strip())
        all_categories_urls.append(f"{constants.url}/" + link_categories.a['href'].strip("./"))

    return all_categories_urls, all_categories_names


def extract_images(link):
    print(link)
    response = parse_html(link)
    images = response.find_all("img")
    for image in images:
        name_image = image['alt'].strip()
        link_image = f'{constants.url}/' + image['src'].lstrip('./')
        with open(name_image.replace(':', '-') + '.jpg', 'wb') as f:
            im = requests.get(link_image)
            f.write(im.content)
            print('Writing: ', name_image)
            print(link_image)


def check_category(links_text):
    print(f"Noms des catégories: {', '.join(get_all_categories_url_and_names()[1])}")
    category = input("Quelle catégorie choisir ? ")
    while category not in get_all_categories_url_and_names()[1]:
        if category == "exit":
            return category
        print("Erreur: Catégorie non disponible dans les catégories")
        print(f"Veuillez choisir dans cette liste: { ', '.join(get_all_categories_url_and_names()[1]) }")
        category = input("Quelle catégorie choisir ? ")
    print(f"Vous sélectionnez { category }")
    return category


def save_books_data_from_category_in_csv(category_url, category):
    """Enregistrer les informations des livres dans un fichier csv"""
    with open(category+'.csv', "w", newline="") as f:
        write = csv.writer(f, delimiter=';')
        write.writerow(["product_page_url", "universal_product_code (upc)", "title", "price_including_tax",
                        "price_excluding_tax", "number_available", "product_description", "category", "review_rating",
                        "image_url"])
        write.writerows(get_data_of_all_books(category_url))


pprint(get_data_of_one_book('https://books.toscrape.com/catalogue/the-golden-condom-and-other-essays-on-love-lost-and-found_637/index.html'))
# pprint(get_data_of_all_books('https://books.toscrape.com/catalogue/category/books/psychology_26/index.html'))
# pprint(get_url_book_from_category('http://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html'))
# display_all_images_in_category('https://books.toscrape.com/catalogue/category/books/sequential-art_5/index.html')
# save_books_data_from_category_in_csv('https://books.toscrape.com/catalogue/category/books/psychology_26/index.html')
# pprint(get_all_categories_url_and_names(constants.url)[1])
# pprint(get_data_of_one_book('https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html')[7])
# print(check_category())
# pprint(get_data_of_one_book('https://books.toscrape.com/catalogue/tipping-the-velvet_999/index.html'))
