# main.py

from gui_canvas import DrawingCanvas
from preprocessing import resample_points
from tangent_angles import process_shape
from fuzzy_filter import fuzzy_filter
from binary_encoding import serial_coding
from bsw_classifier import BSWClassifier
from training_data import X_train, y_train
import numpy as np

if __name__ == "__main__":
    # Initialize classifier
    bsw = BSWClassifier()
    bsw.train(X_train, y_train)

    # Run GUI canvas for shape input
    drawing_app = DrawingCanvas()
    drawing_app.run()

    # Get drawn points and process them
    drawn_points = drawing_app.get_drawn_points()
    resampled_points = resample_points(drawn_points, num_points=64)
    _, tangent_angles = process_shape(resampled_points)

    # Apply fuzzy filtering
    angle_categories = fuzzy_filter(np.degrees(tangent_angles))

    # Convert angles to binary encoding
    binary_input = serial_coding(angle_categories)

    print("Binary Input Shape:", binary_input.shape)  # Should print (32,)

    # Classify the shape
    prediction = bsw.predict(binary_input)
    print("Predicted Shape:", prediction)
