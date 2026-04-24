from dataclasses import dataclass

from PIL import Image


@dataclass
class Palette:
    colors: list[list[int]]
    counts: list[int]

    def sort_by_luminance(self):
        sorted_colors = sorted(
            zip(self.colors, self.counts),
            key=lambda pair: color_luminance(pair[0]),
        )
        self.colors = [color for color, _ in sorted_colors]
        self.counts = [count for _, count in sorted_colors]


def extract_palette(image: Image.Image, num_colors: int = 5) -> Palette:

    quantized: Image.Image = image.quantize(colors=num_colors)

    palette_table: list[int] | None = quantized.getpalette()

    counts: list[tuple[int, int]] | None = quantized.getcolors()

    if palette_table is None or counts is None:
        return Palette([], [])

    sorted_counts = sorted(counts, key=lambda pair: pair[0], reverse=True)
    output_palette: list[tuple[list[int], int]] = []

    for count, index in sorted_counts:
        r = palette_table[index * 3]
        g = palette_table[index * 3 + 1]
        b = palette_table[index * 3 + 2]
        if is_near_white([r, g, b]):
            continue

        output_palette.append(([r, g, b], count))
        if len(output_palette) >= num_colors:
            break

    return Palette(
        [color for color, _ in output_palette], [count for _, count in output_palette]
    )


def is_near_white(color: list[int], threshold: int = 240) -> bool:
    r, g, b = color
    return r >= threshold and g >= threshold and b >= threshold


def color_luminance(color: list[int]) -> float:
    r, g, b = color
    return 0.299 * r + 0.587 * g + 0.114 * b
