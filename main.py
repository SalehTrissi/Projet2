import constants
from Scripting import extract_all_books_informations, extract_all_images, extract_books_from_category, \
    extract_images_from_category
from utils import get_all_categories_url_and_names


def main_menu():
    """affiche le menu principal"""
    print(constants.MENU)
    choice = input("Votre choix : ")
    selection_available = ["1", "2", "3"]
    while choice in selection_available:
        if choice == "1":
            print(constants.Menu_book)
            choice = input("Votre choix : ")
            while choice in selection_available:
                if choice == "1":
                    extract_books_from_category()
                    exit()
                elif choice == "2":
                    extract_all_books_informations()
                    exit()
                elif choice == "3":
                    main_menu()

        elif choice == "2":
            print(constants.Menu_image)
            choice = input("Votre choix : ")
            while choice in selection_available:
                if choice == "1":
                    extract_images_from_category()
                elif choice == "2":
                    extract_all_images()
                elif choice == "3":
                    main_menu()

        elif choice == "3":
            print("Au revoir")
            exit()

    print("Saisi invalide")
    return main_menu()


main_menu()
