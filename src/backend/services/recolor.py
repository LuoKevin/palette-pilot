from PIL import Image


def recolor_from_buckets(
    bucket_map: Image.Image, palette: list[list[int]]
) -> Image.Image:
    if bucket_map.mode != "L":
        raise ValueError(f"Expected grayscale image, got {bucket_map.mode}")

    new_image = Image.new("RGB", bucket_map.size)
    width, height = bucket_map.size
    for y in range(height):
        for x in range(width):
            bucket_index = bucket_map.getpixel((x, y))
            if bucket_index < len(palette):
                new_image.putpixel((x, y), tuple(palette[bucket_index]))
            else:
                new_image.putpixel((x, y), (0, 0, 0))  # Fallback color
    return new_image
