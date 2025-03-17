import tkinter as tk

class DrawingCanvas:
    def __init__(self, width=600, height=600):
        self.width = width
        self.height = height
        self.points = []

        self.root = tk.Tk()
        self.root.title("Shape Drawing Canvas")

        self.canvas = tk.Canvas(self.root, width=self.width, height=self.height, bg="white")
        self.canvas.pack()

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.end_drawing)

        clear_btn = tk.Button(self.root, text="Clear", command=self.clear_canvas)
        clear_btn.pack()

    def start_drawing(self, event):
        self.points = [(event.x, event.y)]
        self.canvas.create_oval(event.x, event.y, event.x + 2, event.y + 2, fill="black")

    def draw(self, event):
        self.points.append((event.x, event.y))
        self.canvas.create_line(self.points[-2][0], self.points[-2][1], event.x, event.y, fill="black", width=2)

    def end_drawing(self, event):
        self.points.append((event.x, event.y))
        # Optionally, visualize final point
        self.canvas.create_oval(event.x, event.y, event.x + 2, event.y + 2, fill="black")

    def clear_canvas(self):
        self.canvas.delete("all")
        self.points.clear()

    def get_drawn_points(self):
        return self.points

    def run(self):
        self.root.mainloop()