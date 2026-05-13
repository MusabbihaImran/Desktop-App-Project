# Deployment

## Installation

1. Ensure you have Python 3.9+ installed.
2. Clone this repository.
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

To run the application from source, execute:
```bash
python main.py
```

## Packaging as an Executable

To package PixelAlchemy as a standalone `.exe` for Windows, you can use PyInstaller.
1. Install PyInstaller: `pip install pyinstaller`
2. Run the build command:
   ```bash
   pyinstaller --noconfirm --onedir --windowed --name "PixelAlchemy"  "main.py"
   ```
3. The packaged app will be available in the `dist/` directory.
