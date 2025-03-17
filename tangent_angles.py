import numpy as np

def build_tangent_vectors(points):
    # Compute tangent vectors between points
    # Ensure points is a numpy array
    points = np.asarray(points)
    
    # Compute differences between consecutive points
    deltas = np.diff(points, axis=0, append=points[:1])
    
    # Normalize the tangent vectors
    norms = np.linalg.norm(deltas, axis=1, keepdims=True)
    tangent_vectors = deltas / norms
    
    return tangent_vectors

def calculate_angles(vectors):
    # Compute angles in degrees between tangent vectors
    angles = np.arctan2(vectors[:, 1], vectors[:, 0])
    return angles

def process_shape(points):
    tangent_vectors = build_tangent_vectors(points)
    tangent_angles = calculate_angles(tangent_vectors)

    return tangent_vectors, tangent_angles
