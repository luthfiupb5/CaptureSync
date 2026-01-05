import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from . import processor

class ImageHandler(FileSystemEventHandler):
    def __init__(self, config):
        self.config = config

    def on_created(self, event):
        if not event.is_directory:
            processor.process_file(event.src_path, self.config)

    def on_moved(self, event):
        # Handle case where file is moved INTO the folder
        if not event.is_directory:
             processor.process_file(event.dest_path, self.config)

def start_to_watch(config):
    source_folder = config.get("source_folder")
    if not source_folder:
        print("No source folder configured.")
        return

    event_handler = ImageHandler(config)
    observer = Observer()
    observer.schedule(event_handler, source_folder, recursive=False)
    observer.start()
    
    print(f"Watching {source_folder} for new images...")
    print("Press Ctrl+C to stop.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
