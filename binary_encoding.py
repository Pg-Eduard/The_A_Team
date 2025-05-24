# binary_encoding.py
import numpy as np

def serial_coding(angle_categories, category_order=['acute', 'right', 'obtuse', 'wide_obtuse'], bins=8):
    total = len(angle_categories)
    counts = [angle_categories.count(cat) / total for cat in category_order]

    binary_vector = []
    for frac in counts:
        bits_on = int(round(frac * bins))
        binary_vector.extend([1]*bits_on + [0]*(bins - bits_on))

    print("Categorized angles:", {cat: angle_categories.count(cat) for cat in ['acute', 'right', 'obtuse', 'wide_obtuse']})

    return np.array(binary_vector)

