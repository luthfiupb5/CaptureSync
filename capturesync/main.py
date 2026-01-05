import json
import os
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.progress import Progress, SpinnerColumn, TextColumn

# Ensure we can import sibling modules if running as script from inside folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from capturesync import watcher
except ImportError:
    # If running directly inside capturesync/
    import watcher

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            pass
    return {}

def save_config(config):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)

def get_valid_path(prompt_text, is_directory=False):
    while True:
        path = input(f"{prompt_text}\n> ").strip().strip('"').strip("'")
        if not path:
            print("Path cannot be empty. Please try again.")
            continue
            
        if is_directory:
            if os.path.isdir(path):
                return path
            else:
                print("Directory not found. Please enter a valid folder path.")
        else:
            if os.path.isfile(path):
                return path
            else:
                print("File not found. Please enter a valid file path.")

def display_startup_animation():
    console = Console()
    
    # Clear screen for fresh start
    console.clear()
    
    # Startup Spinner
    with Progress(
        SpinnerColumn(),
        TextColumn("[bold cyan]Initializing CaptureSync...[/bold cyan]"),
        transient=True,
    ) as progress:
        progress.add_task("init", total=None)
        time.sleep(1.5)  # Simulate loading
        
    # Title and Credits using Panel
    title = Text("CaptureSync CLI v1.1", style="bold magenta justify=center")
    credits = Text("\nDeveloped By Luthfi Bassam U P", style="italic blue justify=center")
    link = Text("https://www.linkedin.com/in/luthfibassamup/", style="underline blue justify=center")
    
    content = Text.assemble(title, "\n", credits, "\n", link, justify="center")
    
    panel = Panel(
        content,
        border_style="cyan",
        padding=(1, 2),
        width=60
    )
    console.print(panel)
    print("") # spacing

def main():
    display_startup_animation()
    # config = load_config() 
    config = {} # Force fresh config every time as per user request
    
    # Check if necessary config exists, else ask
    needs_save = False
    
    # 1. Source Folder
    if not config.get('source_folder') or not os.path.isdir(config.get('source_folder', '')):
        print("\n[Step 1/4] Select SOURCE folder (Camera/Lightroom import)")
        config['source_folder'] = get_valid_path("Enter full path to source folder:", is_directory=True)
        needs_save = True

    # 2. Landscape Overlay
    if not config.get('landscape_overlay') or not os.path.isfile(config.get('landscape_overlay', '')):
        print("\n[Step 2/4] Select LANDSCAPE overlay image (.png)")
        config['landscape_overlay'] = get_valid_path("Enter full path to landscape overlay PNG:", is_directory=False)
        needs_save = True
        
    # 3. Portrait Overlay
    if not config.get('portrait_overlay') or not os.path.isfile(config.get('portrait_overlay', '')):
        print("\n[Step 3/4] Select PORTRAIT overlay image (.png)")
        config['portrait_overlay'] = get_valid_path("Enter full path to portrait overlay PNG:", is_directory=False)
        needs_save = True
        
    # 4. Output Folder
    if not config.get('output_folder') or not os.path.isdir(config.get('output_folder', '')):
        print("\n[Step 4/5] Select OUTPUT folder (Synced to Google Drive)")
        config['output_folder'] = get_valid_path("Enter full path to output folder:", is_directory=True)
        needs_save = True

    # 5. File Prefix (Optional)
    if 'file_prefix' not in config:
        print("\n[Step 5/5] Enter File Prefix (Optional)")
        print("Files will be named like: PREFIX_1.jpg, PREFIX_2.jpg")
        print("Press Enter to skip and keep original filenames.")
        prefix = input("> ").strip().strip('"').strip("'")
        config['file_prefix'] = prefix if prefix else None
        needs_save = True
    
    if needs_save:
        save_config(config)
        print("\nConfiguration saved!")
    else:
        print("\nRefreshed configuration from saved settings.")

    print("\n" + "-"*60)
    print(f"Source:   {config['source_folder']}")
    print(f"Output:   {config['output_folder']}")
    print("-"*60)
    print("Starting process... (Press Ctrl+C to stop)")
    
    watcher.start_to_watch(config)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopping CaptureSync...")
        sys.exit(0)
