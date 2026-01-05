# CaptureSync

**Automated Image Overlay & Cloud Sync Tool**

CaptureSync is a powerful Python automation tool designed for photographers and event organizers. It acts as a real-time bridge between your camera (or Lightroom export folder) and Google Drive, automatically applying branding overlays and syncing files for instant sharing.

## ✨ Features

- **📂 Real-time Watcher**: Instantly detects new images added to a source folder.
- **🖼️ Smart Overlay**: Automatically detects image aspect ratio (Landscape vs Portrait) and applies the correct branding frame.
- **☁️ Instant Sync**: Moves processed images to a designated Output folder (e.g., your Google Drive folder) for immediate cloud upload.
- **🖥️ Beautiful CLI**: Feature-rich terminal interface with status animations and progress tracking.

## 🚀 Prerequisites

1. **Python 3.8+** installed (For manual installation).
2. **Google Drive for Desktop** (or any other cloud sync service like Dropbox/OneDrive) installed and running, so you have a local folder that syncs to the cloud.

## 🛠️ Installation & Usage

### Option 1: Standalone App (Recommended)
**No installation required!** Perfect for photographers and non-developers.
1.  Go to the [Releases](https://github.com/luthfiupb5/CaptureSync/releases) page.
2.  Download `CaptureSync.exe`.
3.  Double-click to run.

### Option 2: Direct Install (For Developers)
If you have Python installed, you can install directly from GitHub without cloning:
```bash
pip install git+https://github.com/luthfiupb5/CaptureSync.git
```
Then simply run:
```bash
capturesync
```

### Option 3: Manual Clone
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/luthfiupb5/CaptureSync.git
    cd CaptureSync
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *Note: This installs `watchdog`, `Pillow`, and `rich`.*

3.  **Run:**
    ```bash
    python capturesync/main.py
    ```

## ⚙️ Configuration (First Run)
The tool will interactively ask you to select:
- **Source Folder**: Where your camera/Lightroom saves images.
- **Landscape Overlay**: Path to your landscape branding .png file.
- **Portrait Overlay**: Path to your portrait branding .png file.
- **Output Folder**: The folder synced with Google Drive.
- **File Prefix** (Optional): Custom prefix for output files (e.g., `PROFILE26` -> `PROFILE26_1.jpg`).

## 👤 Credits

**Developed By Luthfi Bassam U P**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/luthfibassamup/)

---
*Built with ❤️ using Python.*
