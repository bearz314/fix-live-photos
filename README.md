# Fix iPhone 16 Live Photos Metadata Bug

## Overview
This script fixes a bug in **iPhone 16 running iOS 18.0/18.0.1** where Live Photos are not correctly tagged with the `ContentIdentifier` metadata in the accompanying video files. Without this metadata, the Photos app cannot properly combine the still photo and video back into a Live Photo when exported and re-imported.

Apple introduced Live Photos with the **iPhone 6s in 2015**, where a Live Photo consists of:
- A **still photo**.
- A **short video** showing up to 1.5 seconds before and up to 1.5 seconds after the photo.

This script identifies affected video files and fixes the missing `ContentIdentifier` tag by copying it from the corresponding photo file.

📖 [Learn more about Live Photos](https://support.apple.com/en-us/104966)

---

## Problem Description

- **Bug Details**: On **iPhone 16** with **iOS 18.0/18.0.1**, video files captured as part of Live Photos are not tagged with the correct `ContentIdentifier`. This leads to issues when:
  - **Exporting Live Photos** to disk on macOS, where the video does not have the correct metadata.
  - **Re-importing** into Photos app, which cannot recombine the files back into a single Live Photo.
  - **Sharing Live Photos**, causing incompatibilities. [Discussion on Reddit](https://www.reddit.com/r/iphone/comments/1fytijt/bug_when_capturing_live_photos_causing_issues/).

---

## How It Works

The script identifies and fixes video files that meet the following criteria:
1. The file extension is **lowercase `.mov`**.
2. A corresponding image with the **same name but uppercase `.HEIC`** exists.
3. The video is **very short** (less than 5 seconds, which is slightly more than the 3 seconds Apple documented).
4. The video is **missing the `ContentIdentifier` metadata**.

After identification, the script:
- Copies the `ContentIdentifier` from the `.HEIC` file to the `.mov` file.

This ensures the Photos app recognizes and recombines the photo and video into a Live Photo.

---

## Requirements

- Python 3.x
- [ExifTool](https://exiftool.org/) installed on your system.

---

## Installation

### Install ExifTool

#### macOS (Using Homebrew)
1. Install Homebrew if not already installed:
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```
2. Install ExifTool:
   ```bash
   brew install exiftool
   ```

#### Windows
1. Download the ExifTool Windows package from [ExifTool Downloads](https://exiftool.org).
2. Extract the .zip file to a directory (e.g., C:\ExifTool).
3. Add the ExifTool directory to your system's PATH environment variable:
   - Open "Edit System Environment Variables."
   - Add C:\ExifTool to the Path variable.

## Usage

1. **Modify the Path**: Open the script and set the path to your directory containing the `.HEIC` and `.mov` files:
   ```python
   def main():
    # This script will overwrite the files!

    # Path to directory that contains IMG_xxxx.HEIC and IMG_xxxx.mov files
    input_dir_path  = "/path/to/dir/"
   ```
2. **Run the Script**: Run the script using Python:
   ```bash
   python3 fix_live_photos.py
   ```

## Example Output

```
Get metadata for /path/to/dir
Found: /path/to/dir/IMG_0297.mov
Done: /path/to/dir/IMG_0297.mov
Found: /path/to/dir/IMG_0526.mov
Done: /path/to/dir/IMG_0526.mov
Found: /path/to/dir/IMG_0254.mov
Done: /path/to/dir/IMG_0254.mov
Found: /path/to/dir/IMG_0532.mov
Done: /path/to/dir/IMG_0532.mov
Found: /path/to/dir/IMG_0485.mov
Done: /path/to/dir/IMG_0485.mov
Proper live photos:   10
Likely live photos:   5
Restored live photos: 5
```

## Contribution

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
