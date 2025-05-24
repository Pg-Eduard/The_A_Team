import numpy as np

# Define categories: 'acute', 'right', 'obtuse', 'wide_obtuse'
# Each row should have 32 bits: 4 categories × max_count (8)

X_train = np.array([
    # Triangles: mostly acute angles, some right angles, few obtuse, no wide obtuse
    [1,1,1,1,1,0,0,0,  # Acute (5)
     1,0,0,0,0,0,0,0,  # Right (1)
     0,0,0,0,0,0,0,0,  # Obtuse (0)
     0,0,0,0,0,0,0,0], # Wide Obtuse (0)

    [1,1,1,1,0,0,0,0,  # Acute (4)
     1,1,0,0,0,0,0,0,  # Right (2)
     0,0,0,0,0,0,0,0,  # Obtuse (0)
     0,0,0,0,0,0,0,0], # Wide Obtuse (0)

     [1,1,1,1,1,1,0,0,  # Acute (6)
     1,1,0,0,0,0,0,0,  # Right (2)
     0,0,0,0,0,0,0,0,  # Obtuse (0)
     0,0,0,0,0,0,0,0], # Wide Obtuse (0)

    [1,1,1,1,1,0,0,0,  # Acute (5)
     1,1,1,0,0,0,0,0,  # Right (3)
     0,0,0,0,0,0,0,0,  # Obtuse (0)
     0,0,0,0,0,0,0,0], # Wide Obtuse (0)

    # Circles: mostly obtuse and wide obtuse angles
    [0,0,0,0,0,0,0,0,  # Acute (0)
     0,0,0,0,0,0,0,0,  # Right (0)
     1,1,1,1,1,1,1,0,  # Obtuse (7)
     1,1,1,1,1,1,1,1], # Wide Obtuse (8)

    [0,0,0,0,0,0,0,0,  # Acute (0)
     0,0,0,0,0,0,0,0,  # Right (0)
     1,1,1,1,1,1,1,1,  # Obtuse (8)
     1,1,1,1,1,1,1,1], # Wide Obtuse (8)

     [0,0,0,0,0,0,0,0,  # Acute (0)
     0,0,0,0,0,0,0,0,  # Right (0)
     1,1,1,1,1,1,0,0,  # Obtuse (6)
     1,1,1,1,1,1,1,1], # Wide Obtuse (8)

    [0,0,0,0,0,0,0,0,  # Acute (0)
     0,0,0,0,0,0,0,0,  # Right (0)
     1,1,1,1,1,1,1,1,  # Obtuse (8)
     1,1,1,1,1,1,0,0], # Wide Obtuse (6)

    # Rectangles: mostly right angles (4), no acute, obtuse, or wide obtuse
    [0,0,0,0,0,0,0,0,  # Acute (0)
     1,1,1,1,0,0,0,0,  # Right (4)
     0,0,0,0,0,0,0,0,  # Obtuse (0)
     0,0,0,0,0,0,0,0], # Wide Obtuse (0)

    [0,0,0,0,0,0,0,0,  # Acute (0)
     1,1,1,1,1,0,0,0,  # Right (5)
     0,0,0,0,0,0,0,0,  # Obtuse (0)
     0,0,0,0,0,0,0,0], # Wide Obtuse (0)

     [0,0,0,0,0,0,0,0,  # Acute (0)
     1,1,1,1,1,1,0,0,  # Right (6)
     0,0,0,0,0,0,0,0,  # Obtuse (0)
     0,0,0,0,0,0,0,0], # Wide Obtuse (0)

    [0,0,0,0,0,0,0,0,  # Acute (0)
     1,1,1,1,1,1,1,0,  # Right (7)
     0,0,0,0,0,0,0,0,  # Obtuse (0)
     0,0,0,0,0,0,0,0], # Wide Obtuse (0)
])

# Corresponding shape labels
y_train = np.array([
    'Triangle', 'Triangle', 'Triangle', 'Triangle',
    'Circle', 'Circle', 'Circle', 'Circle',
    'Rectangle', 'Rectangle', 'Rectangle', 'Rectangle'
])

y_train = np.array([str(label) for label in y_train])
