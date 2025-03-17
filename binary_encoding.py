# binary_encoding.py
import numpy as np

def serial_coding(angle_categories, category_order=['acute', 'right', 'obtuse', 'wide_obtuse'], max_count=8):
    """
    Convert fuzzy angle categories into a fixed-length binary serial code.
    Ensures that the output vector has exactly 32 elements.
    """
    counts = [angle_categories.count(cat) for cat in category_order]
    
    binary_vector = []
    for count in counts:
        binary_representation = [1]*min(count, max_count) + [0]*(max_count - min(count, max_count))
        binary_vector.extend(binary_representation)

    return np.array(binary_vector)  # Ensures fixed-length 32 output
