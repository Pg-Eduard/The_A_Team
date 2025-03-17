import numpy as np
from scipy.spatial import ConvexHull

def resample_points(points, num_points=64):
    points = np.array(points)
    # Compute cumulative distances between points
    distances = np.sqrt(np.sum(np.diff(points, axis=0)**2, axis=1))
    cumulative_distance = np.insert(np.cumsum(distances), 0, 0)

    # Equally spaced intervals along the perimeter
    interval = np.linspace(0, cumulative_distance[-1], num=num_points, endpoint=False)

    # Interpolation to get evenly spaced points
    new_points = []
    for i in interval:
        idx = np.searchsorted(cumulative_distance, i)
        fraction = (i - cumulative_distance[idx - 1]) / (cumulative_distance[idx] - cumulative_distance[idx - 1])
        new_point = points[idx - 1] + fraction * (points[idx] - points[idx - 1])
        new_points.append(new_point)

    return np.array(new_points)

def calculate_center(points):
    """Calculate the center (centroid) of a shape."""
    points = np.array(points)
    xc = np.mean(points[:, 0])
    yc = np.mean(points[:, 1])
    return np.array([xc, yc])

def remove_crossovers(points):
    """Eliminate crossovers using convex hull to extract significant boundary points."""
    points = np.array(points)
    hull = ConvexHull(points)
    significant_points = points[hull.vertices]
    return significant_points
