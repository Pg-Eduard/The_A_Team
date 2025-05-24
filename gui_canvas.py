import tkinter as tk

class DrawingCanvas:
    def __init__(self, width=600, height=600, predict_callback=None, train_callback=None, classes=None):
        self.width = width
        self.height = height
        self.points = []
        self.predict_callback = predict_callback
        self.train_callback = train_callback
        self.classes = classes or ["Triangle", "Rectangle", "Circle"]

        self.root = tk.Tk()
        self.root.title("Shape Drawing Canvas")

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white")
        self.canvas.pack()

        # Buttons and controls
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        clear_btn = tk.Button(control_frame, text="Clear", command=self.clear_canvas)
        clear_btn.pack(side=tk.LEFT, padx=5)

        predict_btn = tk.Button(control_frame, text="Predict", command=self.predict_shape)
        predict_btn.pack(side=tk.LEFT, padx=5)

        self.result_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.result_label.pack()

        # Label selection for training
        self.label_var = tk.StringVar(value=self.classes[0])
        label_menu = tk.OptionMenu(self.root, self.label_var, *self.classes)
        label_menu.pack(pady=5)

        train_btn = tk.Button(self.root, text="Train on This", command=self.train_on_sample)
        train_btn.pack()

        # Mouse events
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_drawing)

    def start_drawing(self, event):
        self.points = [(event.x, event.y)]
        self.canvas.create_oval(event.x, event.y, event.x + 2, event.y + 2, fill="black")

    def draw(self, event):
        self.points.append((event.x, event.y))
        self.canvas.create_line(self.points[-2][0], self.points[-2][1], event.x, event.y, fill="black", width=2)

    def end_drawing(self, event):
        self.points.append((event.x, event.y))
        self.canvas.create_oval(event.x, event.y, event.x + 2, event.y + 2, fill="black")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points.clear()
        self.result_label.config(text="")

    def predict_shape(self):
        if self.predict_callback and self.points:
            result = self.predict_callback(self.points)
            self.result_label.config(text=f"Predicted: {result}")
        else:
            self.result_label.config(text="Draw a shape first!")

    def train_on_sample(self):
        if self.train_callback and self.points:
            label = self.label_var.get()
            self.train_callback(self.points, label)
            self.result_label.config(text=f"Trained on: {label}")
        else:
            self.result_label.config(text="Draw a shape to train.")

    def run(self):
        self.root.mainloop()
