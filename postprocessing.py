from PIL import Image


def restore_image(path_to_resized_image: str, path_to_restored_image: str, w: int, h: int) -> None:
    Image.open(path_to_resized_image).resize((w, h)).save(path_to_restored_image)
