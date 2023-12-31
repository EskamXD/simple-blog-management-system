from Composite.Component import Component
from Composite.Article import Article
from Database.Database import Database

import os

ARTICLES_PATH = str("data")


class Category(Component):
    def __init__(self, name: str, parent: str or "Category") -> None:
        self.name = name
        self.parent = parent
        self.children = []
        self.path = os.path.join(parent, self.name) if name != "data" else "data"
        self.db = Database(ARTICLES_PATH)

    def add(self, component: Component) -> None:
        self.children.append(component)

    def remove(self, component: Component) -> None:
        self.children.remove(component)

    def operation(self) -> str:
        results = [child.operation() for child in self.children]
        return f"Category({self.name}, {', '.join(results)})"

    def to_dict(self) -> dict:
        children_data = [child.to_dict() for child in self.children]
        return {
            "type": "Category",
            "name": self.name,
            "parent": self.parent,
            "children": children_data,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Category" or "Article":
        try:
            type = data["type"]
        except KeyError:
            raise (KeyError("Missing 'type' key in data dict."))

        if type == "Category":
            name = data["name"]
            parent = data["parent"]
            children = [cls.from_dict(child_data) for child_data in data["children"]]
            category = cls(name, parent)
            category.children = children
            return category
        elif type == "Article":
            return Article.from_dict(data)
        else:
            raise ValueError(f"Invalid type: {type}")

    def save_composite_recursive(self, file_path: str) -> None:
        components_data = self.to_dict()
        self.db.save(file_path, components_data)

    def load_composite_recursive(self, file_path: str) -> None:
        try:
            data = self.db.read(file_path)
        except FileNotFoundError:
            return

        self.name = data["name"]
        self.children = [self.from_dict(child_data) for child_data in data["children"]]
        print(self.children)

    def check_existing_title(self, title: str) -> bool:
        for child in self.children:
            if isinstance(child, Article):
                if child.title == title:
                    return True
        return False
