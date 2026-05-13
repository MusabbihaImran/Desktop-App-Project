# Peer Reviews

## Walkthrough Session
- **What was reviewed**: Overall Tkinter architecture and Database schema (main.py and database.py).
- **Participants**: Lead Developer, UI Designer, Database Admin.
- **Findings**: The database schema needed an `image_type` column for artworks to differentiate between Canvas Art and Generative Patterns in the Gallery. The UI needed to ensure the minimum size was enforced at the root window level.

## Code Inspection
- **Module Reviewed**: `modules/filters_lab.py`
- **Checklist Used**: Memory Leaks, Exception Handling, Code Style (PEP8), Responsiveness.
- **Issues Found**: 
  - Loading corrupted images crashed the app instead of raising a message box.
  - Pillow image objects weren't being correctly sized down for preview, causing memory spikes.
- **Resolution**: Added `try/except` around PIL `Image.open()`, wrapped it in `tkinter.messagebox.showerror`. Added `thumbnail()` resizing before applying filters.

## Pair Review Comments
Throughout the codebase, various inline `# REVIEW` comments have been placed to annotate decisions made during pair programming, verifying logic such as undo/redo limits and numpy array handling.
