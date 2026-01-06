import os
import json
import threading
import customtkinter as ctk
from PIL import Image
try:
    from . import processor, watcher
except ImportError:
    import processor
    import watcher

# Set theme
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

CONFIG_FILE = "gui_config.json"
VERSION = "5.0"

class CaptureSyncApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"CaptureSync v{VERSION}")
        self.geometry("1000x800")

        # Configuration Data
        self.source_var = ctk.StringVar()
        self.landscape_var = ctk.StringVar()
        self.portrait_var = ctk.StringVar()
        self.output_var = ctk.StringVar()
        self.prefix_var = ctk.StringVar(value="fujifilm_x100v_")
        
        # Runtime State
        self.observer = None
        self.running = False
        
        # Progress State
        self.total_files = 0
        self.processed_count = 0

        self.load_config()
        self.create_layout()

    def create_layout(self):
        # Grid Configuration
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # --- HEADER ---
        self.header_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        
        self.logo_label = ctk.CTkLabel(
            self.header_frame, 
            text=f"CaptureSync v{VERSION}", 
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.logo_label.pack(side="left")

        # --- MAIN TABS ---
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        
        self.tab_run = self.tab_view.add("Run")
        self.tab_gallery = self.tab_view.add("Gallery")
        
        # Justify grids for tabs
        self.tab_run.grid_columnconfigure(0, weight=1)
        self.tab_run.grid_rowconfigure(2, weight=1) # Log box expands
        
        self.tab_gallery.grid_columnconfigure(0, weight=1)
        self.tab_gallery.grid_rowconfigure(0, weight=1)

        # === RUN TAB CONTENT ===
        
        # 1. Configuration Section
        self.create_config_section(self.tab_run)

        # 2. Control & Status Section
        self.create_control_section(self.tab_run)

        # 3. Logs
        self.log_box = ctk.CTkTextbox(self.tab_run, height=150, state="disabled")
        self.log_box.grid(row=2, column=0, sticky="nsew", pady=(10, 0))

        # === GALLERY TAB CONTENT ===
        self.gallery_frame = ctk.CTkScrollableFrame(self.tab_gallery, fg_color="transparent")
        self.gallery_frame.grid(row=0, column=0, sticky="nsew")
        self.gallery_images = [] # Keep references
        self.gallery_row = 0
        self.gallery_col = 0
        self.MAX_COLS = 3

        # --- FOOTER ---
        self.footer_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.footer_frame.grid(row=2, column=0, sticky="ew", padx=20, pady=10)

        self.footer_label = ctk.CTkLabel(
            self.footer_frame, 
            text="Developed by Luthfi | LinkedIn: linkedin.com/in/luthfi",
            text_color="gray"
        )
        self.footer_label.pack(side="bottom")

    def create_config_section(self, parent):
        # Helper to create file/folder pickers
        def add_row(container, label_text, variable, command):
            frame = ctk.CTkFrame(container, fg_color="transparent")
            frame.pack(fill="x", pady=5)
            
            lbl = ctk.CTkLabel(frame, text=label_text, width=140, anchor="w")
            lbl.pack(side="left")
            
            entry = ctk.CTkEntry(frame, textvariable=variable)
            entry.pack(side="left", fill="x", expand=True, padx=10)
            
            btn = ctk.CTkButton(frame, text="Browse", width=80, command=command)
            btn.pack(side="right")

        config_frame = ctk.CTkFrame(parent)
        config_frame.grid(row=0, column=0, sticky="ew", pady=10)
        
        ctk.CTkLabel(config_frame, text="Configuration", font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w", padx=10, pady=10)

        add_row(config_frame, "Source Folder:", self.source_var, lambda: self.browse_folder(self.source_var))
        add_row(config_frame, "Output Folder:", self.output_var, lambda: self.browse_folder(self.output_var))
        add_row(config_frame, "Landscape Overlay:", self.landscape_var, lambda: self.browse_file(self.landscape_var))
        add_row(config_frame, "Portrait Overlay:", self.portrait_var, lambda: self.browse_file(self.portrait_var))
        
        # Prefix is just a text entry
        prefix_frame = ctk.CTkFrame(config_frame, fg_color="transparent")
        prefix_frame.pack(fill="x", pady=5)
        ctk.CTkLabel(prefix_frame, text="Filename Prefix:", width=140, anchor="w").pack(side="left")
        ctk.CTkEntry(prefix_frame, textvariable=self.prefix_var).pack(side="left", fill="x", expand=True, padx=10)

    def create_control_section(self, parent):
        control_frame = ctk.CTkFrame(parent)
        control_frame.grid(row=1, column=0, sticky="ew", pady=10)

        # Button Row
        btn_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        btn_frame.pack(fill="x")

        self.start_btn = ctk.CTkButton(
            btn_frame, 
            text="Start Automation", 
            command=self.start_process,
            fg_color="green", hover_color="darkgreen",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.start_btn.pack(side="left", padx=20, pady=20, expand=True, fill="x")

        self.stop_btn = ctk.CTkButton(
            btn_frame, 
            text="Stop", 
            command=self.stop_process,
            state="disabled",
            fg_color="red", hover_color="darkred",
            height=40,
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.stop_btn.pack(side="right", padx=20, pady=20, expand=True, fill="x")

        # Checkbox for Existing Files (v5.0)
        self.process_existing_var = ctk.BooleanVar(value=False)
        self.existing_cb = ctk.CTkCheckBox(control_frame, text="Process Existing Files in Source?", variable=self.process_existing_var)
        self.existing_cb.pack(side="top", pady=(0, 10))

        # Progress Section
        progress_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        progress_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        self.progress_label = ctk.CTkLabel(progress_frame, text="0 / 0 Processed", font=ctk.CTkFont(size=12))
        self.progress_label.pack(side="top", anchor="e")
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.pack(side="bottom", fill="x")
        self.progress_bar.set(0)


    def browse_folder(self, var):
        directory = ctk.filedialog.askdirectory()
        if directory:
            var.set(directory)
            self.save_config()

    def browse_file(self, var):
        filename = ctk.filedialog.askopenfilename(filetypes=[("Images", "*.png;*.jpg;*.jpeg")])
        if filename:
            var.set(filename)
            self.save_config()

    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    self.source_var.set(data.get("source_folder", ""))
                    self.output_var.set(data.get("output_folder", ""))
                    self.landscape_var.set(data.get("landscape_overlay", ""))
                    self.portrait_var.set(data.get("portrait_overlay", ""))
                    self.prefix_var.set(data.get("file_prefix", "fujifilm_x100v_"))
            except Exception:
                pass

    def save_config(self):
        data = {
            "source_folder": self.source_var.get(),
            "output_folder": self.output_var.get(),
            "landscape_overlay": self.landscape_var.get(),
            "portrait_overlay": self.portrait_var.get(),
            "file_prefix": self.prefix_var.get()
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(data, f)

    def log(self, message):
        self.log_box.configure(state="normal")
        self.log_box.insert("end", message + "\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

        # Logic: Detected NEW file -> Increment Total
        if message.startswith("Detected new file:"):
             self.total_files += 1
             self.update_progress_ui()

        # Logic: Successfully processed -> Increment Processed Count & add to gallery
        # "Successfully processed: F:\path\to\file.jpg"
        if message.startswith("Successfully processed: "):
            path = message.replace("Successfully processed: ", "").strip()
            self.processed_count += 1
            self.update_progress_ui()
            self.add_to_gallery(path)

    def update_progress_ui(self):
        self.progress_label.configure(text=f"{self.processed_count} / {self.total_files} Processed")
        if self.total_files > 0:
            val = self.processed_count / self.total_files
            # Clamp to 0-1
            val = max(0.0, min(1.0, val))
            self.progress_bar.set(val)
        else:
            self.progress_bar.set(0)

    def add_to_gallery(self, image_path):
        if not os.path.exists(image_path):
            return

        try:
            # Load and resize for thumbnail
            img = Image.open(image_path)
            img.thumbnail((250, 250)) 
            ctk_img = ctk.CTkImage(light_image=img, dark_image=img, size=img.size)
            
            # Create label
            lbl = ctk.CTkLabel(self.gallery_frame, image=ctk_img, text="")
            lbl.grid(row=self.gallery_row, column=self.gallery_col, padx=10, pady=10)
            
            # Keep ref
            self.gallery_images.append(ctk_img)
            
            # Update grid pos
            self.gallery_col += 1
            if self.gallery_col >= self.MAX_COLS:
                self.gallery_col = 0
                self.gallery_row += 1
                
        except Exception as e:
            print(f"Gallery error: {e}")

    def count_initial_files(self, folder):
        try:
            exts = {".jpg", ".jpeg", ".png"}
            count = 0
            for f in os.listdir(folder):
                if os.path.splitext(f)[1].lower() in exts:
                    # Exclude already processed if they are there (unlikely if source is pure)
                    if "_processed" not in f:
                        count += 1
            return count
        except Exception:
            return 0

    def start_process(self):
        # Basic validation
        if not self.source_var.get() or not self.output_var.get():
            self.log("Error: Source and Output folders are required.")
            return

        if not self.landscape_var.get() and not self.portrait_var.get():
            self.log("Error: At least one Overlay (Landscape or Portrait) is required.")
            return

        self.running = True
        self.start_btn.configure(state="disabled")
        self.stop_btn.configure(state="normal")
        self.existing_cb.configure(state="disabled")
        
        # Reset Progress
        self.processed_count = 0
        src = self.source_var.get()
        
        # If "Process Existing" is checked, we count everything in source.
        # If NOT checked, we start at 0 files (wait for new ones).
        if self.process_existing_var.get():
             self.total_files = self.count_initial_files(src)
        else:
             self.total_files = 0
             
        self.update_progress_ui()

        config = {
            "source_folder": self.source_var.get(),
            "landscape_overlay": self.landscape_var.get(),
            "portrait_overlay": self.portrait_var.get(),
            "output_folder": self.output_var.get(),
            "file_prefix": self.prefix_var.get()
        }
        
        # Thread-safe logger
        def safe_log(msg):
            self.after(0, self.log, msg)

        # 1. Process Existing Files (if checked)
        if self.process_existing_var.get():
            safe_log("Scanning for existing files...")
            threading.Thread(target=self.process_existing_files, args=(config, safe_log)).start()

        # 2. Start watcher
        safe_log("Starting automation...")
        self.observer = watcher.start_watcher(
            self.source_var.get(), 
            config,
            log_callback=safe_log 
        )

    def process_existing_files(self, config, log_callback):
        source = config['source_folder']
        try:
            files = sorted(os.listdir(source))
            # Don't increment total_files here as we pre-calculated it in start_process
            for filename in files:
                 if not self.running: # STOP LOGIC FIX
                     log_callback("Stopped processing existing files.")
                     break
                     
                 filepath = os.path.join(source, filename)
                 if os.path.isfile(filepath):
                     processor.process_file(filepath, config, log_callback)
            
            if self.running:
                log_callback(f"Finished processing existing files.")
                
        except Exception as e:
            log_callback(f"Error scanning existing files: {e}")

    def stop_process(self):
        self.running = False # Flag to stop loop
        
        if self.observer:
            self.observer.stop()
            # self.observer.join() # Don't block UI
        
        self.log("Automation stopped.")
        self.start_btn.configure(state="normal")
        self.stop_btn.configure(state="disabled")
        self.existing_cb.configure(state="normal")

if __name__ == "__main__":
    app = CaptureSyncApp()
    app.mainloop()
