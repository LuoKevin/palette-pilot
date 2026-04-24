from PIL import Image


def extract_palette(image: Image.Image, num_colors: int = 5) -> list[list]:
    return [[255, 255, 255]] * num_colors