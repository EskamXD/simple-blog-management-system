from BlogManagement.BlogManagement import BlogManagement
from Composite.Category import Category
from Composite.Article import Article
from Database import Database
from Strategy.ValidationStrategy import ValidationStrategy
from Strategy.MetaTitleValidator import MetaTitleValidator
from Strategy.MetaDescriptionValidator import MetaDescriptionValidator
from Strategy.ImageSizeValidator import ImageSizeValidator
from Strategy.ArticleStatusChanger import ArticleStatusChanger


ARTICLES_PATH = str("data")


class Terminal(BlogManagement):
    def __init__(self, db: "Database", root: "Category") -> None:
        self.db = db
        self.root = root

        # Load state from JSON
        try:
            self.root.load_composite_recursive("main_state.json")
        except FileNotFoundError:
            pass

    def save_and_exit(self) -> None:
        # Save state to JSON
        # for component in self.root.children:
        #     component.save_composite_recursive(
        #         f"{ARTICLES_PATH}/{component.name}/articles_info.json"
        #     )
        self.root.save_composite_recursive("main_state.json")

        exit()

    def run(self) -> None:
        choice_dict = {
            "1": self.add_article,
            "2": self.show_articles,
            "3": self.update_status,
            "4": self.show_categories,
            "5": self.show_titles,
            "6": self.print_composite,
            "-1": self.save_and_exit,
        }

        while True:
            print("\nMenu:")
            print("1. Add article")
            print("2. Show articles")
            print("3. Update status")
            print("4. Show categories")
            print("5. Show titles")
            print("6. Print composite")
            print("-1. Save & Exit")

            choice = input("Enter your choice (1-6): ")

            choice_dict.get(
                choice, lambda: print("Invalid choice. Please try again.")
            )()

    def add_article(self) -> None:
        # Wyświetl dostępne kategorie
        category_components_dict = {
            category_object: category_object.name
            for category_object in self.root.children
        }
        print(
            f"Available categories: {[category_name for category_name in category_components_dict.values()]}"
        )

        # Pobierz kategorię
        category = self.user_input("Enter category name: ")
        for category_object, category_name in category_components_dict.items():
            if category_name == category:
                category_component = category_object

        # Sprawdź, czy wpisana kategoria istnieje
        if category_component is None:
            print(f"Category '{category}' does not exist.")
            return

        # Wyświetl dostępne tytuły w danej kategorii
        article_titles = [
            article_object.title for article_object in category_component.children
        ]
        if article_titles:
            print(
                f"Existing titles in category '{category_component.name}': {article_titles}"
            )
        else:
            print(f"No articles in category '{category_component.name}'.")

        # Pobierz tytuł artykułu
        title = self.user_input("Enter article title: ", MetaTitleValidator())

        # Sprawdź, czy taki tytuł już istnieje w danej kategorii
        if category_component.check_existing_title(title):
            print(
                f"Article '{title}' already exists in category '{category_component.name}'."
            )
            return

        # Pobierz treść artykułu
        content = self.user_input(
            "Enter article content (can_be_null=True): ", can_be_null=True
        )

        # Pobierz ścieżkę do obrazka
        image_path = self.user_input(
            "Enter image path (can_be_null=True): ", None, True
        )

        try:
            # Jeśli ścieżka do obrazka została podana, skopiuj obrazek do folderu z kategorią
            new_image_path = ""
            if image_path != "":
                new_image_path = self.db.copy_image(image_path, category_component, title)
                
            ImageSizeValidator().validate(new_image_path)
        except FileNotFoundError:
            print("Image not found.")
            return
        except ValueError:
            print("Image size is too big.")
            return
        except Exception as e:
            print(e)
            return

        # Pobierz status artykułu
        status = self.user_input_status(ArticleStatusChanger())

        # Pobierz meta description
        meta_description = self.user_input(
            "Enter meta description: ", MetaDescriptionValidator()
        )

        # Stwórz obiekt artykułu
        article_component = Article(
            title,
            content,
            new_image_path,
            status,
            meta_description,
            category_component.name,
        )
        # Dodaj artykuł do kategorii
        category_component.add(article_component)

        # Zapisz stan do DOCX i JSON
        article_component.save(category_component)
        # category_component.save_composite_recursive(
        #     f"{ARTICLES_PATH}/{category_component.name}/articles_info.json"
        # )
        self.root.save_composite_recursive("main_state.json")

        print(f"Article '{title}' added to category '{category_component.name}'.")

    def show_articles(self) -> None:
        # Wyświetl dostępne kategorie
        category_components_dict = {
            category_object: category_object.name
            for category_object in self.root.children
        }
        print(
            f"Available categories: {[category_name for category_name in category_components_dict.values()]}"
        )

        # Pobierz kategorię
        category = self.user_input("Enter category name: ")
        for category_object, category_name in category_components_dict.items():
            if category_name == category:
                category_component = category_object

        # Sprawdź, czy wpisana kategoria istnieje
        if category_component is None:
            print(f"Category '{category}' does not exist.")
            return

        # Wyświetl dostępne tytuły w danej kategorii
        article_objects = [
            article_object.title for article_object in category_component.children
        ]
        if article_objects:
            print(
                f"Existing titles in category '{category_component.name}': {article_objects}"
            )
        else:
            print(f"No articles in category '{category_component.name}'.")

    def update_status(self) -> None:
        # Wyświetl dostępne kategorie
        category_components_dict = {
            category_object: category_object.name
            for category_object in self.root.children
        }
        print(
            f"Available categories: {[category_name for category_name in category_components_dict.values()]}"
        )

        # Pobierz kategorię
        category = self.user_input("Enter category name: ")
        for category_object, category_name in category_components_dict.items():
            if category_name == category:
                category_component = category_object

        # Sprawdź, czy wpisana kategoria istnieje
        if category_component is None:
            print(f"Category '{category}' does not exist.")
            return

        # Wyświetl dostępne tytuły w danej kategorii
        article_titles = [
            article_object.title for article_object in category_component.children
        ]
        if article_titles:
            print(
                f"Existing titles in category '{category_component.name}': {article_titles}"
            )
        else:
            print(f"No articles in category '{category_component.name}'.")
            return

        title = self.user_input("Enter article title: ")

        new_status = self.user_input_status(ArticleStatusChanger())

        articles = [articles for articles in category_component.children]
        for article in articles:
            if article.title == title:
                article.status = new_status
                article.save(category_component)
                break

        # Zapisz stan do DOCX i JSON
        # category_component.save_composite_recursive(
        #     f"{ARTICLES_PATH}/{category_component.name}/articles_info.json"
        # )
        self.root.save_composite_recursive("main_state.json")

        print(f"Article '{title}' added to category '{category_component.name}'.")

    def show_categories(self) -> None:
        # Wyświetl dostępne kategorie
        category_components_dict = {
            category_object: category_object.name
            for category_object in self.root.children
        }
        print(f"Available categories: {list(category_components_dict.values())}")
        return category_components_dict

    def show_titles(self) -> None:
        category_components_dict = self.show_categories()
        titles_list = []

        for category_component, category_name in category_components_dict.items():
            titles_list.append(
                [article_object.title for article_object in category_component.children]
            )

        print(f"All titles list: {titles_list}")
        return titles_list

    def user_input(
        self,
        input_placeholder: str,
        validator_function: "ValidationStrategy" = None,
        can_be_null: bool = False,
    ) -> str:
        user_input = input(input_placeholder)
        while type(user_input) == str and len(user_input) < 1 and not can_be_null:
            validator_function.validate(user_input)
            user_input = input(input_placeholder)

        return user_input.strip()

    def user_input_status(self, status_validator: "ValidationStrategy") -> str:
        user_input = ""
        while user_input == "":
            # while type(user_input) == str and len(user_input) < 1:
            user_input = input(f"Enter article status [Draft, Ready to publish, Published] (Draft): ")
            user_input = status_validator.validate(user_input)

        return user_input

    def print_composite(self) -> None:
        print(self.root.operation())
