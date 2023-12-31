from Composite import Category

import json
import os
import shutil

ARTICLES_PATH = str("data")


class Database:
    _instance = None

    def __new__(cls, data_path: str) -> "Database":
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cls._instance.data_path = data_path
            if not os.path.exists(cls._instance.data_path):
                os.makedirs(cls._instance.data_path)
        return cls._instance

    def save(self, file_path: str, data: dict or list or str) -> None:
        with open(file_path, "w", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)

    def append(self, file_path: str, data: dict or list or str) -> None:
        with open(file_path, "a", encoding="utf-8") as json_file:
            json.dump(data, json_file, indent=4)

    def read(self, file_path: str) -> dict or list or str:
        try:
            with open(file_path, "r", encoding="utf-8") as json_file:
                data = json.load(json_file)
        except FileNotFoundError:
            return FileNotFoundError
        return data

    def copy_image(image_path: str, category_component: "Category", title: str) -> None:
        current_path = os.path.dirname(os.path.abspath(__file__))
        new_image_path = os.path.join(
            current_path,
            f"{ARTICLES_PATH}/{category_component.name}",
            f"images/{title}.jpg",
        )

        shutil.copyfile(image_path, new_image_path)

        return new_image_path
