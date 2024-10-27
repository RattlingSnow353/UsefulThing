import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD

replace_color = (73, 218, 76)
layout_image = Image.open(r"img\image.png").convert("RGBA")

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Useful Thing Probably")
        self.canvas = tk.Canvas(root, width=1000, height=100)
        self.canvas.pack()
        self.placeholder_image = None
        self.final_image = None
        self.processed_image = None
        self.btn_open = tk.Button(root, text="Open Placeholder Image", command=self.load_image)
        self.btn_open.pack()
        self.btn_save = tk.Button(root, text="Save Final Image", command=self.save_image)
        self.btn_save.pack()
        self.label = tk.Label(root, text="Drag and drop your image onto the canvas or use the button above.")
        self.label.pack()
        self.canvas.drop_target_register(DND_FILES)
        self.canvas.dnd_bind('<<Drop>>', self.drop)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
        if file_path:
            self.canvas.delete("all")
            self.final_image = None
            self.process_image(file_path)

    def process_image(self, file_path):
        self.canvas.delete("all")
        self.final_image = None
        self.placeholder_image = Image.open(file_path).convert("RGBA")
        target_color_pixel_position = (34, 52)
        target_color = self.placeholder_image.getpixel(target_color_pixel_position)
        ace = self.placeholder_image.crop((0, 5, 71, 96))
        corner_symbol = self.placeholder_image.crop((90, 6, 99, 16))
        p_card = self.placeholder_image.crop((87, 29, 100, 42))
        prominent_color = self.get_most_prominent_solid_color(ace)
        self.processed_image = self.replace_color_in_image(layout_image, replace_color, prominent_color)
        self.add_images_to_layout(self.processed_image, ace, corner_symbol, p_card)
        self.display_final_image(self.processed_image)

    def get_most_prominent_solid_color(self, image):
        colors = image.getcolors(image.size[0] * image.size[1])
        solid_colors = [(count, color) for count, color in colors if color[3] == 255]
        if solid_colors:
            most_common_color = max(solid_colors, key=lambda item: item[0])
            return most_common_color[1]
        return None

    def replace_color_in_image(self, image, original_color, new_color):
        pixels = image.load()
        for x in range(image.width):
            for y in range(image.height):
                if pixels[x, y][:3] == original_color:
                    pixels[x, y] = new_color
        return image

    def add_images_to_layout(self, layout_image, ace, corner_symbol, p_card):
        layout_image.paste(ace, (852, 0), ace)
        corner_positions_top = [(x - 95, 17) for x in range(100, 1000, 71)]
        corner_positions_bottom = [(x - 43, 69) for x in reversed(range(100, 1000, 71))]
        for pos in corner_positions_top:
            layout_image.paste(corner_symbol, pos, corner_symbol)
        corner_symbol_flipped = corner_symbol.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT)
        for pos in corner_positions_bottom:
            layout_image.paste(corner_symbol_flipped, pos, corner_symbol_flipped)
        p_card_positions = [
            (29, 12), (100, 12), (100, 42), (160, 12), (182, 12),
            (160 + 71, 12), (182 + 71, 12), (182 + 71 - 11, 42), (160 + 71 * 2, 12), (182 + 71 * 2, 12),
            (160 + 71 * 2, 42), (182 + 71 * 2, 42), (160 + 71 * 3, 12), (182 + 71 * 3, 12), (160 + 71 * 3, 42),
            (182 + 71 * 3, 42),
            (182 + 71 * 3 - 11, 26), (160 + 71 * 4, 42), (182 + 71 * 4, 42), (160 + 71 * 4, 12), (182 + 71 * 4, 12),
            (182 + 71 * 4 - 11, 26), (160 + 71 * 5, 12), (182 + 71 * 5, 12), (160 + 71 * 6, 12), (182 + 71 * 6, 12),
            (160 + 71 * 5, 34), (182 + 71 * 5, 34), (160 + 71 * 6, 34), (182 + 71 * 6, 34), (182 + 71 * 6 - 11, 23),
            (182 + 71 * 5 - 11, 23)
        ]
        for pos in p_card_positions:
            layout_image.paste(p_card, pos, p_card)
        p_card_flipped = p_card.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.FLIP_LEFT_RIGHT)
        r_p_card_positions = [
            (29, 70), (100, 70), (160, 70), (182, 70), (160 + 71, 70), (182 + 71, 70),
            (160 + 71 * 2, 70), (182 + 71 * 2, 70), (160 + 71 * 3, 70), (182 + 71 * 3, 70),
            (160 + 71 * 4, 70), (182 + 71 * 4, 70), (182 + 71 * 4 - 11, 55), (160 + 71 * 5, 70), (182 + 71 * 5, 70),
            (160 + 71 * 6, 70), (182 + 71 * 6, 70),
            (160 + 71 * 6, 48), (182 + 71 * 6, 48), (160 + 71 * 5, 48), (182 + 71 * 5, 48), (182 + 71 * 6 - 11, 60)
        ]
        for pos in r_p_card_positions:
            layout_image.paste(p_card_flipped, pos, p_card_flipped)

    def display_final_image(self, layout_image):
        self.canvas.delete("all")
        self.final_image = ImageTk.PhotoImage(layout_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.final_image)

    def save_image(self):
        self.canvas.delete("all")  # Clear the canvas before saving the image
        if self.processed_image:  # Use the processed image to save
            file_path = filedialog.asksaveasfilename(defaultextension=".png",
                                                     filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if file_path:
                self.processed_image.save(file_path)  # Save the processed image directly
                messagebox.showinfo("Success", "Image saved successfully!")
        else:
            messagebox.showwarning("No Image", "Please process an image before saving.")

    def drop(self, event):
        file_path = event.data
        self.process_image(file_path)

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()