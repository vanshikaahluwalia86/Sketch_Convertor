import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

def pencil_sketch(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print("Image not found.")
        return None

    gra = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    gra = clahe.apply(gra)

    invert = cv2.bitwise_not(gra)
    blur = cv2.GaussianBlur(invert, (21, 21), 0)
    inverted_blur = cv2.bitwise_not(blur)
    sketch = cv2.divide(gra, inverted_blur, scale=256.0)

    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    sketch = cv2.filter2D(sketch, -1, kernel)

    return sketch

def open_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp")])
    if file_path:
        sketch = pencil_sketch(file_path)
        if sketch is not None:
            show_sketch(sketch)

def show_sketch(sketch):
    img_rgb = cv2.cvtColor(sketch, cv2.COLOR_GRAY2RGB)
    img_pil = Image.fromarray(img_rgb)

    # Get screen size and resize if needed
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    max_width = screen_width - 100
    max_height = screen_height - 100
    if img_pil.width > max_width or img_pil.height > max_height:
        img_pil.thumbnail((max_width, max_height), Image.LANCZOS)

    img_tk = ImageTk.PhotoImage(img_pil)

    top = tk.Toplevel()
    top.title("Pencil Sketch Result")
    # Center the window
    x = (screen_width - img_pil.width) // 2
    y = (screen_height - img_pil.height) // 2
    top.geometry(f"{img_pil.width}x{img_pil.height}+{x}+{y}")

    lbl = tk.Label(top, image=img_tk)
    lbl.image = img_tk  # Keep a reference!
    lbl.pack()

# Main GUI window
root = tk.Tk()
root.title("Pencil Sketch Generator")

frame = tk.Frame(root, padx=20, pady=20)
frame.pack()

label = tk.Label(frame, text="Upload an image to create a pencil sketch", font=("Arial", 14))
label.pack(pady=10)

btn = tk.Button(frame, text="Choose Image", command=open_image, font=("Arial", 12))
btn.pack()

root.mainloop()
