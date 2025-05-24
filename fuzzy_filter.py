import numpy as np

def categorize_angle(angle_deg):
    if angle_deg < 60:
        return 'acute'
    elif 60 <= angle_deg < 105:
        return 'right'
    elif 105 <= angle_deg < 150:
        return 'obtuse'
    else:
        return 'wide_obtuse'

def fuzzy_filter(tangent_angles_rad):
    angles_deg = np.abs(np.degrees(tangent_angles_rad)) % 180
    categories = [categorize_angle(angle) for angle in angles_deg]
    counts = {cat: categories.count(cat) for cat in ['acute', 'right', 'obtuse', 'wide_obtuse']}
    print("Categorized angles:", counts)
    return categories
