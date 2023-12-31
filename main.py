from BlogManagement.GUI import GUI
from BlogManagement.Terminal import Terminal
from Composite.Category import Category
from Database.Database import Database

ARTICLES_PATH = str("data")


if __name__ == "__main__":
    blog_management = GUI(Database(ARTICLES_PATH), Category("data", "data"))

    blog_management.run()
