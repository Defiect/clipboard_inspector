import win32clipboard
import win32con

def get_all_clipboard_formats():
    """
    Enumerates all formats currently on the clipboard and prints them.
    Also demonstrates how to retrieve data for a specific format (text).
    """

    # A dictionary to map common clipboard format IDs to human-readable names.
    # You can find a full list of standard formats here:
    # https://docs.microsoft.com/en-us/windows/win32/dataxchg/standard-clipboard-formats
    format_map = {
        win32con.CF_TEXT: "CF_TEXT",
        win32con.CF_BITMAP: "CF_BITMAP",
        win32con.CF_DIB: "CF_DIB",
        win32con.CF_DIBV5: "CF_DIBV5",
        win32con.CF_DSPBITMAP: "CF_DSPBITMAP",
        win32con.CF_DSPENHMETAFILE: "CF_DSPENHMETAFILE",
        win32con.CF_DSPMETAFILEPICT: "CF_DSPMETAFILEPICT",
        win32con.CF_DSPTEXT: "CF_DSPTEXT",
        win32con.CF_ENHMETAFILE: "CF_ENHMETAFILE",
        win32con.CF_HDROP: "CF_HDROP (File List)",
        win32con.CF_LOCALE: "CF_LOCALE",
        win32con.CF_METAFILEPICT: "CF_METAFILEPICT",
        win32con.CF_OEMTEXT: "CF_OEMTEXT",
        win32con.CF_OWNERDISPLAY: "CF_OWNERDISPLAY",
        win32con.CF_PALETTE: "CF_PALETTE",
        win32con.CF_PENDATA: "CF_PENDATA",
        win32con.CF_PRIVATEFIRST: "CF_PRIVATEFIRST",
        win32con.CF_PRIVATELAST: "CF_PRIVATELAST",
        win32con.CF_RIFF: "CF_RIFF",
        win32con.CF_SYLK: "CF_SYLK",
        win32con.CF_TIFF: "CF_TIFF",
        win32con.CF_WAVE: "CF_WAVE",
        win32con.CF_UNICODETEXT: "CF_UNICODETEXT (Unicode Text)",
    }
    # Add reverse mapping for easy lookup
    for key, value in list(format_map.items()):
        format_map[value] = key


    print("Inspecting clipboard...")
    print("-" * 30)

    try:
        # Open the clipboard
        win32clipboard.OpenClipboard()

        print("Available formats on the clipboard:")
        
        # Enumerate over all available formats
        current_format = 0
        while True:
            # The EnumClipboardFormats function retrieves the format identifier
            # of the next available clipboard format in the list.
            current_format = win32clipboard.EnumClipboardFormats(current_format)
            if current_format == 0:
                # A return value of 0 means we've reached the end of the list
                break
            
            # Look up the format name from our map
            format_name = format_map.get(current_format, f"UNKNOWN_FORMAT ({current_format})")
            print(f"  - {format_name}")
            
            # --- Demonstrate getting data for a specific format ---
            # If the format is Unicode text, let's try to get and print it.
            if current_format == win32con.CF_UNICODETEXT:
                try:
                    data = win32clipboard.GetClipboardData(win32con.CF_UNICODETEXT)
                    print(f"    [Data for CF_UNICODETEXT]:\n---\n{data}\n---")
                except Exception as e:
                    print(f"    [Could not get data for this format: {e}]")
            
            # If the format is a file list (e.g., from copying a file in Explorer)
            if current_format == win32con.CF_HDROP:
                try:
                    files = win32clipboard.GetClipboardData(win32con.CF_HDROP)
                    print(f"    [Data for CF_HDROP (Files)]: ")
                    for f in files:
                        print(f"      - {f}")
                except Exception as e:
                    print(f"    [Could not get data for this format: {e}]")


    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        # Always make sure to close the clipboard
        win32clipboard.CloseClipboard()

    print("-" * 30)


if __name__ == "__main__":
    # --- Instructions for testing ---
    # 1. Run the script once after copying some plain text.
    # 2. Copy a file (or multiple files) in Windows Explorer and run the script again.
    # 3. Copy a rich text selection from Word or an image from a web browser and run it again.
    
    get_all_clipboard_formats()