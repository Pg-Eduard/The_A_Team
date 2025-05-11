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
    def __init__(self, master=None, text="",justify="left",anchor="e", **kwargs):
        super().__init__(master, **kwargs)

        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(self, text=text, wraplength=480, justify=justify,anchor=anchor)
        self.label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Shape Classifier")
        self.geometry("520x700")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(6, weight=0)

        # Clasificator
        self.classifier = BSWClassifier()
        self.classifier.train(X_train, y_train)

        # Frame titlu lung
        self.titlu = CustomFrame(
            self,
            text="Neuro-fuzzy system for Geometric Shape recognition: "
                 "on-line shape recognition from hand-drawn shapes",
            justify="center"
        )
        self.titlu.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))

        # Canvas container
        self.canvas_container = ctk.CTkFrame(self)
        self.canvas_container.grid(row=2, column=0, padx=10, pady=5, sticky="nsew")

        self.drawing_title= ctk.CTkLabel(master=self.canvas_container,text="Deseneaza o forma:",font=ctk.CTkFont(size=20,weight="bold"))
        self.drawing_title.pack()

        self.tk_canvas_frame = tk.Frame(self.canvas_container, bg="white", width=400, height=400)
        self.tk_canvas_frame.pack()

        self.drawing_canvas = DrawingCanvas(master=self.tk_canvas_frame, width=400, height=400, bg="white")
        self.drawing_canvas.pack()

        # Butoane
        self.slot_butoane = CustomFrame(self,text="",width=400)
        self.slot_butoane.grid(row=3,column=0,pady=10,padx=10,sticky="nsew")

        self.classify_button = ctk.CTkButton(master=self.slot_butoane, text="Clasifică Forma", command=self.classify_shape)
        self.classify_button.grid(row=0, column=0, pady=(20, 10), padx=10)

        self.result_label = ctk.CTkLabel(master=self.slot_butoane, text="Rezultatul va apărea aici.", font=ctk.CTkFont(size=16))
        self.result_label.grid(row=1, column=0, pady=(5, 10), padx=10)

        self.clear_button = ctk.CTkButton(master=self.slot_butoane, text="Șterge Canvas", command=self.clear_canvas)
        self.clear_button.grid(row=2, column=0, pady=(0, 15), padx=10)

        #Footer
        self.footer = CustomFrame(
            self,
            text="Proiectantii:" \
            "\nDeac Melinda Anca" \
            "\nIvan Luiza Elena" \
            "\nPopescu George-Eduard" ,
            justify="center",
            anchor="center"
        )
        self.footer.grid(row=6,column=0,pady=20,sticky="ew")

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

        self.result_label.configure(text=f"Formă prezisă: {prediction}")

    def clear_canvas(self):
        self.drawing_canvas.clear()


if __name__ == "__main__":
    app = App()
    app.mainloop()
