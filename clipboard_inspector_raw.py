import win32clipboard
import win32con
import re
import os
import time

def save_hex_dump(data, filename):
    """
    Saves raw bytes to a file for viewing in a hex editor.
    """
    try:
        with open(filename, 'wb') as f:
            # If the data is not in byte form, convert it to bytes
            if not isinstance(data, (bytes, memoryview)):
                # Convert to string representation and encode as UTF-8
                byte_data = str(data).encode('utf-8')
            else:
                byte_data = bytes(data)
            
            f.write(byte_data)
    except Exception as e:
        print(f"      [!] Failed to write raw bytes to {filename}: {e}")

def inspect_and_dump_clipboard():
    """
    Enumerates all formats on the clipboard, prints them to the console,
    and saves the raw data for each format to a .hex file.
    """
    # A dictionary to map common clipboard format IDs to human-readable names.
    format_map = {
        win32con.CF_TEXT: "CF_TEXT", win32con.CF_BITMAP: "CF_BITMAP",
        win32con.CF_DIB: "CF_DIB", win32con.CF_DIBV5: "CF_DIBV5",
        win32con.CF_DSPBITMAP: "CF_DSPBITMAP", win32con.CF_DSPENHMETAFILE: "CF_DSPENHMETAFILE",
        win32con.CF_DSPMETAFILEPICT: "CF_DSPMETAFILEPICT", win32con.CF_DSPTEXT: "CF_DSPTEXT",
        win32con.CF_ENHMETAFILE: "CF_ENHMETAFILE", win32con.CF_HDROP: "CF_HDROP_FileList",
        win32con.CF_LOCALE: "CF_LOCALE", win32con.CF_METAFILEPICT: "CF_METAFILEPICT",
        win32con.CF_OEMTEXT: "CF_OEMTEXT", win32con.CF_OWNERDISPLAY: "CF_OWNERDISPLAY",
        win32con.CF_PALETTE: "CF_PALETTE", win32con.CF_PENDATA: "CF_PENDATA",
        win32con.CF_PRIVATEFIRST: "CF_PRIVATEFIRST", win32con.CF_PRIVATELAST: "CF_PRIVATELAST",
        win32con.CF_RIFF: "CF_RIFF", win32con.CF_SYLK: "CF_SYLK",
        win32con.CF_TIFF: "CF_TIFF", win32con.CF_WAVE: "CF_WAVE",
        win32con.CF_UNICODETEXT: "CF_UNICODETEXT",
    }

    print("Inspecting clipboard and dumping all formats to .hex files...")
    print("-" * 60)

    try:
        # Open the clipboard to read its contents
        win32clipboard.OpenClipboard()

        print("Available formats on the clipboard:")
        
        current_format = 0
        formats_found = False
        while True:
            # Enumerate over all available formats
            current_format = win32clipboard.EnumClipboardFormats(current_format)
            if current_format == 0:
                # Reached the end of the list
                break
            
            formats_found = True
            
            # Look up the format name, creating a fallback for unknown custom formats
            format_name = format_map.get(current_format, f"UNKNOWN_FORMAT_{current_format}")
            print(f"  - Found format: {format_name}")
            
            try:
                # Attempt to retrieve the data for the current format
                data = win32clipboard.GetClipboardData(current_format)
                
                # Sanitize the format name to create a valid filename
                safe_filename = re.sub(r'[^a-zA-Z0-9_]', '', format_name)
                
                
                timestamp = int(time.time())
                
                output_filename = f"clipboard_dump_{timestamp}_{safe_filename}.hex"
                
                print(f"    > Dumping data to {output_filename}")
                save_hex_dump(data, output_filename)

            except Exception as e:
                # It's common to fail getting data for some formats (e.g., synthesized ones)
                print(f"    > Could not retrieve data for this format: {e}")
        
        if not formats_found:
            print("  No formats found on the clipboard.")

    except Exception as e:
        print(f"\nAn error occurred: {e}")
    finally:
        # Always make sure to close the clipboard
        win32clipboard.CloseClipboard()

    print("-" * 60)
    print("Dump complete. Check for '.hex' files in this script's directory.")
    print(f"Directory: {os.getcwd()}")


if __name__ == "__main__":
    # --- Instructions for testing ---
    # 1. Copy some plain text and run this script.
    # 2. Copy a file (or multiple files) in Windows Explorer and run this script again.
    # 3. Copy a rich text selection from Word/Wordpad or an image from a web browser and run it again.
    inspect_and_dump_clipboard()
