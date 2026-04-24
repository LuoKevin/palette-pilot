# palette-pilot

## AI Engineering Notes

### Palette extraction: raw signal vs heuristic filtering

The MVP starts with a simple, classical image-processing approach: extract dominant RGB colors from the reference image using quantization. This gives a raw color signal, but raw dominance is not the same thing as semantic usefulness.

For example, a reference image may be mostly white background and black lineart, while the useful character colors occupy fewer pixels:

```text
80% white background
10% black lineart
5% skin
3% hair
2% clothing
```

Raw palette extraction may correctly return white and black as dominant colors, but those may be poor choices for recoloring character regions.

This creates an important heuristic tradeoff:

```text
raw signal = faithful to pixel distribution
filtered signal = easier to use, but based on assumptions
```

For the MVP, any filtering should be explicit and isolated in small functions. A reasonable first heuristic is to filter near-white colors, because large white backgrounds are common. More aggressive filters, such as removing near-black or low-saturation colors, can accidentally remove useful colors like black hair, dark clothing, gray outfits, or shadows.

The goal is not to pretend the heuristic is universally correct. The goal is to make the assumption visible, testable, and easy to change.
