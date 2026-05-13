import unittest
import numpy as np
import tkinter as tk
from modules.pattern_maker import PatternMaker

class TestPatterns(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.app = PatternMaker(self.root)

    def tearDown(self):
        self.root.destroy()

    def test_waves_output(self):
        # 10. Test waves returns numpy array of correct shape
        arr = self.app._gen_waves(100, 100, 5.0, 0)
        self.assertIsInstance(arr, np.ndarray)
        self.assertEqual(arr.shape, (100, 100, 3))
        self.assertEqual(arr.dtype, np.uint8)

    def test_checkerboard_output(self):
        # 11. Test checkerboard bounds
        arr = self.app._gen_checkerboard(50, 50, 5.0, 0)
        self.assertEqual(arr.shape, (50, 50, 3))
        self.assertTrue(np.all((arr >= 0) & (arr <= 255)))

    def test_mandala_output(self):
        # 12. Test mandala shape
        arr = self.app._gen_mandala(60, 60, 2.0, 50)
        self.assertEqual(arr.shape, (60, 60, 3))

    def test_truchet_output(self):
        # 13. Test truchet type
        arr = self.app._gen_truchet(100, 100, 5.0, 0)
        self.assertEqual(arr.dtype, np.uint8)

if __name__ == "__main__":
    unittest.main()
