from tkinter import *
from tkinter import messagebox
from MakeGif import MakeGif
from tkinter.filedialog import askopenfilenames


class MakeGUI:
    def __init__(self, tk_root: Tk):
        self.images = []
        self.gif = None
        self.frame = Frame(tk_root)
        self.body = LabelFrame(self.frame)
        self.preview = LabelFrame(self.frame)

        self.nameStr = StringVar()
        self.durationVar = DoubleVar()
        self.images_count = IntVar()
        self.manual_height = IntVar()
        self.manual_width = IntVar()

        self.resizeLargest = BooleanVar()
        self.resizeLargest.set(True)

        self.resizeSmallest = BooleanVar()
        self.resizeSmallest.set(False)

        # design stuff
        Label(self.body, text="GIF Name: ").grid(row=0, column=0, sticky=W, pady=2)
        self.name_entry = Entry(self.body, textvariable=self.nameStr, width=25, borderwidth=2, relief="groove")
        self.name_entry.grid(row=0, column=1, sticky=W, pady=2)
        self.name_entry.focus_set()

        # pictures input
        self.images_files = Button(self.body, text="Select Images")
        self.images_files.bind("<Button-1>", self.get_images)
        self.images_files.grid(row=2, column=0, sticky=W, pady=6)

        Label(self.body, text="Images: ").grid(row=3, column=0, sticky=W, pady=2)
        self.chosen_images_count = Label(self.body, textvariable=self.images_count, background="light grey", width=21,
                                         justify="left", anchor="w")
        self.chosen_images_count.grid(row=3, column=1, sticky=W, pady=2)
        self.images_count.set(0)  # default

        Label(self.body, text="Duration: ").grid(row=4, column=0, sticky=W, pady=2)
        self.duration_entry = Entry(self.body, textvariable=self.durationVar, width=25, borderwidth=2, relief="groove")
        self.duration_entry.grid(row=4, column=1, sticky=W, pady=2)
        self.durationVar.set(1.0)  # one second default

        # resize options
        Label(self.body, text="Auto Resize: ").grid(row=5, column=0, sticky=W, pady=2)
        Checkbutton(self.body, text="Fit to Largest", variable=self.resizeLargest).grid(row=5, column=1,
                                                                                        sticky=W, pady=2)
        Checkbutton(self.body, text="Fit to Smallest", variable=self.resizeSmallest).grid(row=6, column=1,
                                                                                          sticky=W, pady=2)

        # manual resize
        Label(self.body, text="Manual Resize: ").grid(row=7, column=0, sticky=W, pady=2)

        Label(self.body, text="Height: ").grid(row=8, column=0, sticky=W, pady=2)
        self.height_entry = Entry(self.body, textvariable=self.manual_height, width=25, borderwidth=2, relief="groove")
        self.height_entry.grid(row=8, column=1, sticky=W, pady=2)

        Label(self.body, text="Width: ").grid(row=9, column=0, sticky=W, pady=2)
        self.width_entry = Entry(self.body, textvariable=self.manual_width, width=25, borderwidth=2, relief="groove")
        self.width_entry.grid(row=9, column=1, sticky=W, pady=2)

        # create gif button
        self.create_gif = Button(self.body, text="Create Gif")
        self.create_gif.bind("<Button-1>", self.create_gif_file)
        self.create_gif.grid(row=10, column=1, sticky=W, pady=8)

        self.body.pack(side=TOP, fill=BOTH)
        self.preview.pack(side=TOP, fill=BOTH)
        self.frame.pack()

    def get_images(self, event=None):
        self.images = askopenfilenames(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.webp *.bmp *.tiff")])
        self.images_count.set(len(self.images))

    def create_gif_file(self, event=None):
        if self.nameStr.get() == "":
            messagebox.showerror("No save name entered", "Please enter a name for the gif.")
            return

        if len(self.images) == 0:
            messagebox.showerror("No images selected", "Please select images.")
            return

        if not self.nameStr.get().endswith(".gif"):
            self.nameStr.set(self.nameStr.get() + ".gif")

        gif = MakeGif(self.nameStr.get(), '../Created Gifs')
        gif.set_images(self.images)

        converted_duration = int(self.durationVar.get() * 1000)

        if self.manual_height.get() > 0 and self.manual_width.get() > 0:
            created_gif = gif.make_gif(converted_duration,
                                       manual_size=(self.manual_height.get(), self.manual_width.get()))
        else:
            created_gif = gif.make_gif(converted_duration,
                                       resize_largest=self.resizeLargest.get(),
                                       resize_smallest=self.resizeSmallest.get())

        # show message
        messagebox.showinfo("Gif Created", f"Gif created at {created_gif}")


def main():
    root = Tk()
    root.title('GIF Maker v1.0')
    root.resizable(width=False, height=False)

    MakeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
