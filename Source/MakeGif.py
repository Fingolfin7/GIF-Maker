import os
from PIL import Image, ImageSequence


class MakeGif:
    def __init__(self, name, path=""):
        self.name = name
        self.path = path
        self.temp_path = os.path.join(self.path, 'temp')
        self.__images = []

    def set_images(self, images: list):
        if not os.path.isdir(self.temp_path):
            os.makedirs(self.temp_path)

        for image in images:
            try:
                # create a copy of the image in the temp folder to avoid overwriting the original
                with Image.open(image) as img:
                    new_path = os.path.join(self.temp_path, os.path.basename(image))
                    img.save(new_path)
                    self.__images.append(new_path)
            except Exception as e:
                print("Failed to open image: ", e)

    def resize_images(self, size: tuple[int, int]):
        for image in self.__images:
            img = Image.open(image)
            img = img.resize(size)
            img.save(image)

    def __find_largest(self):
        sizes = []
        for image in self.__images:
            sizes.append(Image.open(image).size)
        largest = max(sizes)
        return largest

    def __find_smallest(self):
        sizes = []
        for image in self.__images:
            sizes.append(Image.open(image).size)
        smallest = min(sizes)
        return smallest


    def make_gif(self, duration: int, manual_size: tuple[int, int] = None,
                 resize_largest: bool = False, resize_smallest: bool = False):
        frames = []

        if resize_largest:
            largest = self.__find_largest()
            self.resize_images(largest)

        if resize_smallest:
            smallest = self.__find_smallest()
            self.resize_images(smallest)

        if manual_size:
            self.resize_images(manual_size)

        if not os.path.isdir(self.path):
            os.makedirs(self.path)

        for image in self.__images:
            frames.append(Image.open(image))
        frames[0].save(os.path.join(self.path, self.name), format='GIF', append_images=frames[1:],
                       save_all=True, duration=duration, loop=0)

        # return the gif path
        return os.path.join(self.path, self.name)

    # destructor method to clean up the temp folder
    def __del__(self):
        if os.path.isdir(self.temp_path):
            for file in os.listdir(self.temp_path):
                os.remove(os.path.join(self.temp_path, file))
            os.rmdir(self.temp_path)