import numpy as np

def categorize_angle(angle_deg):
    """
    Categorize angle (in degrees) into fuzzy categories.
    """
    if angle_deg < 45:
        return 'acute'
    elif 45 <= angle_deg <= 90:
        return 'right'
    elif 90 < angle_deg <= 135:
        return 'obtuse'
    else:
        return 'wide_obtuse'

def fuzzy_filter(tangent_angles_rad):
    """
    Categorize tangent angles using fuzzy logic.
    """
    angles_deg = np.abs(np.degrees(tangent_angles_rad))
    categories = [categorize_angle(angle) for angle in angles_deg]
    return categories
