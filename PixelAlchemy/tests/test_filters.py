import unittest
from PIL import Image, ImageOps
import tkinter as tk
from modules.filters_lab import FiltersLab

class TestFilters(unittest.TestCase):
    def setUp(self):
        # Create a small RGB image for testing
        self.img = Image.new('RGB', (10, 10), color=(255, 0, 0)) # solid red image
        self.root = tk.Tk()
        self.app = FiltersLab(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_grayscale(self):
        # 6. Test grayscale conversion
        gray_img = ImageOps.grayscale(self.img).convert("RGB")
        self.assertEqual(gray_img.mode, "RGB")
        # Grayscale of solid red
        r, g, b = gray_img.getpixel((0, 0))
        self.assertEqual(r, g)
        self.assertEqual(g, b)

    def test_invert(self):
        # 7. Test invert
        inv_img = ImageOps.invert(self.img)
        r, g, b = inv_img.getpixel((0, 0))
        self.assertEqual((r, g, b), (0, 255, 255))

    def test_sepia(self):
        # 8. Test sepia manually applied formula
        sepia_img = self.app._apply_sepia(self.img.copy())
        r, g, b = sepia_img.getpixel((0, 0))
        # 0.393*255 = 100
        self.assertTrue(90 <= r <= 110)

    def test_pixelate(self):
        # 9. Test pixelate returns an image of the same size
        pix_img = self.app._apply_pixelate(self.img.copy())
        self.assertEqual(pix_img.size, (10, 10))

if __name__ == "__main__":
    unittest.main()
