import numpy as np
from gui_canvas import DrawingCanvas
from preprocessing import resample_points
from tangent_angles import process_shape
from fuzzy_filter import fuzzy_filter
from binary_encoding import serial_coding
from bsw_classifier import BSWClassifier
from training_data import X_train, y_train
from collections import Counter

X_data = list(X_train)
y_data = list(y_train)

bsw = BSWClassifier()
bsw.train(np.array(X_data), np.array(y_data))

def heuristic_guess(binary_input):
    acute = sum(binary_input[0:8])
    right = sum(binary_input[8:16])
    obtuse = sum(binary_input[16:24])
    wide = sum(binary_input[24:32])

    if acute >= 5 and right < 3 and obtuse < 2:
        return "Triangle"
    elif right >= 4 and acute <= 1 and obtuse <= 1:
        return "Rectangle"
    elif obtuse >= 5 or wide >= 5:
        return "Circle"
    return None

def predict(points):
    resampled_points = resample_points(points, num_points=64)
    _, tangent_angles = process_shape(resampled_points)
    angle_categories = fuzzy_filter(np.degrees(tangent_angles))
    binary_input = serial_coding(angle_categories)

    print(f"Angle counts (A, R, O, W): {[
        sum(binary_input[0:8]), 
        sum(binary_input[8:16]), 
        sum(binary_input[16:24]), 
        sum(binary_input[24:32])
    ]}")

    label = heuristic_guess(binary_input)

    if not label:
        prediction = bsw.predict(binary_input)
        label = prediction[0].item() if isinstance(prediction[0], np.generic) else prediction[0]

    return label

def train_new_sample(points, label):
    resampled_points = resample_points(points, num_points=64)
    _, tangent_angles = process_shape(resampled_points)
    angle_categories = fuzzy_filter(np.degrees(tangent_angles))
    binary_input = serial_coding(angle_categories)

    X_data.append(binary_input)
    y_data.append(str(label))

    print(X_data)
    print(y_data)

    bsw.train(np.array(X_data), np.array(y_data))
    print(f"Added training sample: {label}")

def evaluate_training_set():
    print("\n--- TRAINING SET EVALUATION ---")
    correct = 0
    for x, label in zip(X_data, y_data):
        pred = bsw.predict(x)[0]
        pred_str = pred.item() if isinstance(pred, np.generic) else pred
        match = pred_str == label
        print(f"True: {label}, Pred: {pred_str}", "✔️" if match else "❌")
        if match:
            correct += 1
    print(f"Accuracy: {correct}/{len(y_data)} = {correct / len(y_data):.2%}")

if __name__ == "__main__":
    print("--- Training Set Summary ---")
    print(Counter(y_data))
    evaluate_training_set()

    drawing_app = DrawingCanvas(
        predict_callback=predict,
        train_callback=train_new_sample,
        classes=["Triangle", "Rectangle", "Circle"]
    )
    drawing_app.run()
