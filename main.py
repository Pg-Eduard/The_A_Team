import customtkinter as ctk
import tkinter as tk
import numpy as np
from preprocessing import resample_points
from tangent_angles import process_shape
from fuzzy_filter import fuzzy_filter
from binary_encoding import serial_coding
from bsw_classifier import BSWClassifier
from training_data import X_train, y_train


class DrawingCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<B1-Motion>", self.draw)
        self.bind("<ButtonRelease-1>", self.finish_drawing)
        self.points = []

    def draw(self, event):
        x, y = event.x, event.y
        self.points.append((x, y))
        r = 2
        self.create_oval(x - r, y - r, x + r, y + r, fill="black")

    def finish_drawing(self, event):
        pass

    def get_drawn_points(self):
        return self.points

    def clear(self):
        self.delete("all")
        self.points = []


class CustomFrame(ctk.CTkFrame):
    def __init__(self, master=None, text="", justify="center", anchor="center", **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(
            self,
            text=text,
            wraplength=480,
            justify=justify,
            anchor=anchor
        )
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="n")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Shape Classifier")
        self.geometry("520x800")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(6, weight=0)

        self.classifier = BSWClassifier()
        self.X_data = list(X_train)
        self.y_data = list(y_train)
        self.classifier.train(np.array(self.X_data), np.array(self.y_data))

        self.titlu = CustomFrame(
            self,
            text="Neuro-fuzzy system for Geometric Shape recognition: "
                 "on-line shape recognition from hand-drawn shapes",
            justify="center",
            anchor="center"
        )
        self.titlu.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))

        self.canvas_container = ctk.CTkFrame(self)
        self.canvas_container.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        self.drawing_title = ctk.CTkLabel(
            master=self.canvas_container,
            text="Desenează o formă:",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.drawing_title.pack()

        self.tk_canvas_frame = tk.Frame(self.canvas_container, bg="white", width=400, height=400)
        self.tk_canvas_frame.pack()

        self.drawing_canvas = DrawingCanvas(master=self.tk_canvas_frame, width=400, height=400, bg="white")
        self.drawing_canvas.pack()

        self.slot_butoane = CustomFrame(self, text="", width=400)
        self.slot_butoane.grid(row=3, column=0, pady=10, padx=10, sticky="nsew")

        self.classify_button = ctk.CTkButton(master=self.slot_butoane, text="Clasifică Forma", command=self.classify_shape)
        self.classify_button.grid(row=0, column=0, pady=(20, 10), padx=10)

        self.result_label = ctk.CTkLabel(master=self.slot_butoane, text="Rezultatul va apărea aici.", font=ctk.CTkFont(size=16))
        self.result_label.grid(row=1, column=0, pady=(5, 10), padx=10)

        self.clear_button = ctk.CTkButton(master=self.slot_butoane, text="Șterge Canvas", command=self.clear_canvas)
        self.clear_button.grid(row=2, column=0, pady=(0, 15), padx=10)

        self.training_section = ctk.CTkFrame(self)
        self.training_section.grid(row=4, column=0, padx=10, pady=10, sticky="nsew")
        self.training_section.grid_columnconfigure(0, weight=1)

        self.training_label = ctk.CTkLabel(
            master=self.training_section,
            text="Adaugă desenul la setul de antrenare:",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="center",
            justify="center"
        )
        self.training_label.grid(row=0, column=0, pady=(10, 5), padx=10)

        self.train_triangle_button = ctk.CTkButton(
            master=self.training_section,
            text="Adaugă ca Triunghi",
            command=lambda: self.train_with_label("Triangle")
        )
        self.train_triangle_button.grid(row=1, column=0, pady=5, padx=10)

        self.train_rectangle_button = ctk.CTkButton(
            master=self.training_section,
            text="Adaugă ca Dreptunghi",
            command=lambda: self.train_with_label("Rectangle")
        )
        self.train_rectangle_button.grid(row=2, column=0, pady=5, padx=10)

        self.train_circle_button = ctk.CTkButton(
            master=self.training_section,
            text="Adaugă ca Cerc",
            command=lambda: self.train_with_label("Circle")
        )
        self.train_circle_button.grid(row=3, column=0, pady=5, padx=10)

        self.evaluate_button = ctk.CTkButton(
            master=self.training_section,
            text="Evaluează setul de antrenament",
            command=self.evaluate_training_data
        )
        self.evaluate_button.grid(row=4, column=0, pady=(10, 15), padx=10)

        self.footer = CustomFrame(
            self,
            text="Proiectanții:\nDeac Melinda Anca\nIvan Luiza Elena\nPopescu George-Eduard",
            justify="center",
            anchor="center"
        )
        self.footer.grid(row=6, column=0, pady=20, sticky="ew")

    def classify_shape(self):
        points = self.drawing_canvas.get_drawn_points()
        if not points:
            self.result_label.configure(text="Nu s-a desenat nimic.")
            return

        resampled = resample_points(points, num_points=64)
        _, tangent_angles = process_shape(resampled)
        angle_categories = fuzzy_filter(np.degrees(tangent_angles))
        binary_input = serial_coding(angle_categories)
        prediction = self.classifier.predict(binary_input)

        predicted_label = prediction[0].item() if isinstance(prediction[0], np.generic) else str(prediction[0])
        self.result_label.configure(text=f"Formă prezisă: {predicted_label}")

    def clear_canvas(self):
        self.drawing_canvas.clear()

    def train_with_label(self, label):
        points = self.drawing_canvas.get_drawn_points()
        if not points:
            self.result_label.configure(text="Desenul este gol.")
            return

        resampled = resample_points(points, num_points=64)
        _, tangent_angles = process_shape(resampled)
        angle_categories = fuzzy_filter(np.degrees(tangent_angles))
        binary_input = serial_coding(angle_categories)

        self.X_data.append(binary_input)
        self.y_data.append(label)
        self.classifier.train(np.array(self.X_data), np.array(self.y_data))
        self.result_label.configure(text=f"Desen adăugat ca '{label}'.")

    def evaluate_training_data(self):
        correct = 0
        for x, label in zip(self.X_data, self.y_data):
            pred = self.classifier.predict(x)[0]
            pred_str = pred.item() if isinstance(pred, np.generic) else pred
            if pred_str == label:
                correct += 1
        total = len(self.y_data)
        acc = correct / total * 100
        self.result_label.configure(text=f"Acuratețe pe setul de antrenament: {acc:.2f}%")


if __name__ == "__main__":
    app = App()
    app.mainloop()
