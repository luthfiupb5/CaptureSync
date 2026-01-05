# CaptureSync

**Automated Image Overlay & Cloud Sync Tool**

CaptureSync is a powerful Python automation tool designed for photographers and event organizers. It acts as a real-time bridge between your camera (or Lightroom export folder) and Google Drive, automatically applying branding overlays and syncing files for instant sharing.

## ✨ Features

- **📂 Real-time Watcher**: Instantly detects new images added to a source folder.
- **🖼️ Smart Overlay**: Automatically detects image aspect ratio (Landscape vs Portrait) and applies the correct branding frame.
- **☁️ Instant Sync**: Moves processed images to a designated Output folder (e.g., your Google Drive folder) for immediate cloud upload.
- **🖥️ Beautiful CLI**: Feature-rich terminal interface with status animations and progress tracking.

## 🚀 Prerequisites

1. **Python 3.8+** installed.
2. **Google Drive for Desktop** (or any other cloud sync service like Dropbox/OneDrive) installed and running, so you have a local folder that syncs to the cloud.

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/CaptureSync.git
   cd CaptureSync
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: This installs `watchdog`, `Pillow`, and `rich`.*

## 📖 Usage

1. **Run the application:**
   ```bash
   python capturesync/main.py
   ```

2. **First-time Setup:**
   The tool will interactively ask you to select:
   - **Source Folder**: Where your camera/Lightroom saves images.
   - **Landscape Overlay**: Path to your landscape branding .png file.
   - **Portrait Overlay**: Path to your portrait branding .png file.
   - **Output Folder**: The folder synced with Google Drive.

3. **Start Shooting:**
   Simply drop images into the Source Folder. CaptureSync will process them and they will appear in your Output Folder, ready for sharing!

## 👤 Credits

**Developed By Luthfi Bassam U P**

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/luthfibassamup/)

---
*Built with ❤️ using Python.*
