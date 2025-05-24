from gui_canvas import DrawingCanvas
from preprocessing import resample_points
from tangent_angles import process_shape
from fuzzy_filter import fuzzy_filter
from binary_encoding import serial_coding
from bsw_classifier import BSWClassifier
from training_data import X_train, y_train
import numpy as np

bsw = BSWClassifier()
bsw.train(X_train, y_train)

def predict(points):
    resampled_points = resample_points(points, num_points=64)
    _, tangent_angles = process_shape(resampled_points)
    angle_categories = fuzzy_filter(np.degrees(tangent_angles))
    binary_input = serial_coding(angle_categories)
    prediction = bsw.predict(binary_input)
    print(prediction)
    if isinstance(prediction, (list, np.ndarray)) and len(prediction) > 0:
        return prediction[0].item() 
    else:
        return "Unknown"

if __name__ == "__main__":
    drawing_app = DrawingCanvas(predict_callback=predict)
    drawing_app.run()
