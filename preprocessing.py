from PIL import Image


def resize_image(path_to_image: str, path_to_resized_image: str) -> tuple:
    image = Image.open(path_to_image)
    w, h = image.size
    image.resize((416, 416)).save(path_to_resized_image)
    return w, h
