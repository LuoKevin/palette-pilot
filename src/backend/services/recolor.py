from PIL import Image


def recolor_image(
    bucket_map: Image.Image,
    luminance_img: Image.Image,
    palette: list[list[int]],
    lineart_threshold: int = 30,
    min_shade: float = 0.45,
) -> Image.Image:
    if bucket_map.mode != "L":
        raise ValueError(f"Expected grayscale image, got {bucket_map.mode}")
    if luminance_img.mode != "L":
        raise ValueError(f"Expected grayscale image, got {luminance_img.mode}")
    if bucket_map.size != luminance_img.size:
        raise ValueError("bucket_map and luminance_img must have the same dimensions")

    new_image = Image.new("RGB", bucket_map.size)
    width, height = bucket_map.size
    for y in range(height):
        for x in range(width):
            bucket_index = bucket_map.getpixel((x, y))
            new_pixel = (0, 0, 0)  # Default to black if bucket index is out of range
            if bucket_index < len(palette):
                luminance_pixel = luminance_img.getpixel((x, y))
                if luminance_pixel >= lineart_threshold:
                    base_color = palette[bucket_index]
                    luminance_multiplier = min_shade + (1 - min_shade) * luminance_pixel / 255
                    new_pixel = tuple(int(c * luminance_multiplier) for c in base_color)

            new_image.putpixel((x, y), new_pixel)
    return new_image
