import os
import constants
from utils import parse_html, get_data_of_all_books, get_all_categories_url_and_names, extract_images, check_category, \
    save_books_data_from_category_in_csv


def extract_images_from_category():
    try:
        os.mkdir(os.getcwd() + '/images')
        os.chdir(os.getcwd() + "/images")
        os.mkdir(os.path.join(os.getcwd()))
    except:
        pass
    os.chdir(os.path.join(os.getcwd() + "/images"))
    links = get_all_categories_url_and_names()[0]
    links_text = get_all_categories_url_and_names()[1]
    category = check_category(links_text)
    print(category)
    if category == "exit":
        print("You choose to exit program. Good bye !")
        exit()
    index = [link_text
             for link_text in links_text].index(category)
    category_url = links[index]
    extract_images(category_url)


def extract_all_images():
    try:
        os.mkdir(os.getcwd() + '/all images')
        os.chdir(os.getcwd() + "/all images")
        os.mkdir(os.path.join(os.getcwd()))
    except:
        pass
    os.chdir(os.path.join(os.getcwd() + "/all images"))
    links = get_all_categories_url_and_names()[0]
    for link in links:
        extract_images(link)


def extract_books_from_category():
    links = get_all_categories_url_and_names()[0]
    links_text = get_all_categories_url_and_names()[1]
    category = check_category(links_text)
    if category == "exit":
        print("You choose to exit program. Good bye !")
        exit()
    index = [link_text
             for link_text in links_text].index(category)
    category_url = links[index]
    get_data_of_all_books(category_url)
    save_books_data_from_category_in_csv(category_url, category)


def extract_all_books_informations():
    response = parse_html(constants.url)
    all_links_categorys = []
    links = response.find('ul', {"class": "nav nav-list"}).find('ul').find_all('li')
    for link in links:
        all_links = f"{constants.url}/" + link.a['href']
        all_links_categorys.append(all_links)
        get_data_of_all_books(all_links)
        save_books_data_from_category_in_csv(all_links)


# pprint(extract_all_books_informations('https://books.toscrape.com/index.html'))
# extract_all_images('https://books.toscrape.com/catalogue/category/books/travel_2/index.html', 'all images')
# extract_images_from_category()
