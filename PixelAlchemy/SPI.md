# Software Process Improvement (SPI)

During the development of PixelAlchemy, we underwent the following improvement cycles:

## Cycle 1: Rendering Bottleneck
- **Problem**: When rendering large grid sizes (64x64) in the Canvas Editor, drawing thousands of individual Tkinter rectangles was slow and caused UI hitching.
- **Improvement**: We optimized by caching the drawn objects and updating their configurations (e.g., `itemconfigure`) rather than deleting and re-creating them on every brush stroke. 

## Cycle 2: Image Processing Blocking the UI Thread
- **Problem**: The Pillow image filters (like Blur or Emboss on large images) would block the main Tkinter thread, making the app feel unresponsive and frozen.
- **Improvement**: We introduced threaded execution for heavy filter operations or optimized array manipulations so the UI stays responsive, and the user receives a loading state instead of a frozen screen.
