# Clipboard Inspector

A Windows clipboard analysis tool that dumps all clipboard formats for inspection. Includes two versions: one for human-readable hex dumps and another for raw binary files.

## Features

- Enumerates all available clipboard formats
- Two output modes:
  - Human-readable hex dumps with ASCII representation
  - Raw binary data for hex editor analysis
- Handles various data types (text, images, files, etc.)
- Timestamped output files in `dumps/` directory

## Requirements

- Windows OS
- Python 3.x
- `pywin32` package

## Installation

```bash
pip install pywin32
```

## Usage

1. Copy something to your clipboard (text, file, image, etc.)
2. Choose your preferred script:
   
   **For human-readable hex dumps:**
   ```bash
   python clipboard_inspector.py
   ```
   Creates `.txt` files in `dumps/` directory with formatted hex dumps including addresses and ASCII representation.

   **For raw binary data (hex editor analysis):**
   ```bash
   python clipboard_inspector_raw.py
   ```
   Creates `.hex` files in the current directory containing pure binary data for hex editor inspection.

## Output

**clipboard_inspector.py** creates files as `dumps/clipboard_dump_{timestamp}_{format}.txt` with formatted hex dumps.

**clipboard_inspector_raw.py** creates files as `clipboard_dump_{timestamp}_{format}.hex` with raw binary data.

Where:
- `timestamp`: Unix timestamp when the dump was created
- `format`: Clipboard format name (e.g., CF_TEXT, CF_UNICODETEXT, CF_HDROP_FileList)

Perfect for reverse engineering clipboard data formats and understanding how different applications store clipboard content.
