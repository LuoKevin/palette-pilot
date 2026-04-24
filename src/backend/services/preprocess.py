from PIL import Image


def compute_luminance(image: Image.Image) -> Image.Image:
    mode = image.mode
    if mode != "RGB":
        raise ValueError(f"Expected RGB image, got {mode}")

    grayscale_image = image.convert("L")
    return grayscale_image


def create_tone_bucket_map(
    grayscale_image: Image.Image, num_buckets: int = 5
) -> Image.Image:
    if grayscale_image.mode != "L":
        raise ValueError(f"Expected grayscale image, got {grayscale_image.mode}")
    bucket_map = grayscale_image.point(lambda p: p * num_buckets // 256)
    return bucket_map


def visualize_tone_buckets(
    tone_buckets: Image.Image, num_buckets: int = 5
) -> Image.Image:
    if tone_buckets.mode != "L":
        raise ValueError(f"Expected grayscale image, got {tone_buckets.mode}")
    if num_buckets <= 1:
        raise ValueError("num_buckets must be greater than 1")

    return tone_buckets.point(lambda p: p * 255 // (num_buckets - 1))


def create_tone_bucket_debug_image(
    image: Image.Image, num_buckets: int = 5
) -> Image.Image:
    if num_buckets <= 1:
        raise ValueError("num_buckets must be greater than 1")
    luminance_image = compute_luminance(image)
    bucket_map = create_tone_bucket_map(luminance_image, num_buckets)
    return visualize_tone_buckets(bucket_map, num_buckets)
