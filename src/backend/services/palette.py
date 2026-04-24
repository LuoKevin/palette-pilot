from PIL import Image

class Palette:
    def __init__(self, colors: list[list[int]], counts: list[int]):
        self.colors = colors
        self.counts = counts


def extract_palette(image: Image.Image, num_colors: int = 5) -> Palette:

    quantized : Image.Image = image.quantize(colors=num_colors)

    palette_table : list[int] | None = quantized.getpalette()

    counts : list[tuple[int, int]] | None = quantized.getcolors()

    if palette_table is None or counts is None:
        return Palette([], [])

    sorted_counts : list[tuple[int, int]] = sorted(counts, key=lambda x: x[0], reverse=True)

    output_palette : list[list[int]] = []

    for count, index in sorted_counts[:num_colors]:
        r = palette_table[index * 3]
        g = palette_table[index * 3 + 1]
        b = palette_table[index * 3 + 2]
        output_palette.append([r, g, b])

    return Palette(output_palette, [count for count, _ in sorted_counts[:num_colors]])
