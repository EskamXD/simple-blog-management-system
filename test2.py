from os import listdir, rmdir, path, mkdir
import os


if not os.path.exists("categories"):
    os.makedirs("categories")

root_dir = "categories"
folders = [category for category in listdir(
    root_dir) if path.isdir(path.join(root_dir, category))]


for folder in folders:
    if not os.listdir(path.join(root_dir, folder)):
        os.makedirs(path.join(root_dir, folder, "images"))
        os.makedirs(path.join(root_dir, folder, "images\\original"))
        os.makedirs(path.join(root_dir, folder, "images\\webp"))
        os.makedirs(path.join(root_dir, folder,
                    "images\\thumbnails_webp"))

    else:
        if not os.listdir(path.join(root_dir, folder, "images")):
            os.makedirs(path.join(root_dir, folder, "images\\original"))
            os.makedirs(path.join(root_dir, folder, "images\\webp"))
            os.makedirs(path.join(root_dir, folder,
                        "images\\thumbnails_webp"))

image_count = {}
count = 0

for folder in folders:
    files = listdir(path.join(root_dir, folder, "images\\webp"))
    for file in files:
        if file[-4:] == "webp":
            count += 1

    image_count.update({folder: count})
