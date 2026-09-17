import os
import io
import tkinter as tk
from tkinter import filedialog, ttk
from mutagen import File as MutagenFile
from PIL import Image, ImageTk

class MediaViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Player - Day 3")
        self.root.geometry("900x560")
        self.root.config(bg="#1e1e1e")

        # Application State Lists
        self.playlist = []
        self.filtered_list = []
        self.current_image_ref = None # Prevents garbage collection of album art photos

        # Top Menu Bar
        menu_bar = tk.Menu(self.root)
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open Media...", command=self.add_files)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        self.root.config(menu=menu_bar)

        # Left Panel (Display Area & Controls)
        left_panel = tk.Frame(self.root, bg="#1e1e1e")
        left_panel.pack(side="left", fill="both", padx=20, pady=20)

        # Right Panel (Playlist & Search)
        right_panel = tk.Frame(self.root, bg="#1e1e1e")
        right_panel.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Display Frame Container (Fixed Size for Album Art/Video)
        self.display_frame = tk.Frame(left_panel, bg="#2d2d2d", width=300, height=240)
        self.display_frame.pack(pady=(0, 15))
        self.display_frame.pack_propagate(False)

        self.art_label = tk.Label(
            self.display_frame, 
            text="🎵\nNo Media Loaded", 
            font=("Arial", 14, "bold"), 
            bg="#2d2d2d", 
            fg="#aaaaaa"
        )
        self.art_label.pack(fill="both", expand=True)

        # Progress Slider Placeholder
        self.progress_slider = ttk.Scale(left_panel, from_=0, to=100, orient="horizontal")
        self.progress_slider.pack(fill="x", pady=(0, 15))

        # Control Buttons Container
        btn_frame = tk.Frame(left_panel, bg="#1e1e1e")
        btn_frame.pack()
        
        btn_styles = {"bg": "#333333", "fg": "#ffffff", "bd": 0, "padx": 10, "pady": 6, "font": ("Arial", 10)}
        for text in ["⏮ Prev", "▶ Play", "⏹ Stop", "⏭ Next"]:
            tk.Button(btn_frame, text=text, **btn_styles).pack(side="left", padx=4)

        # Search Bar & Add Media Button
        search_frame = tk.Frame(right_panel, bg="#1e1e1e")
        search_frame.pack(fill="x", pady=(0, 8))

        tk.Label(search_frame, text="Search:", bg="#1e1e1e", fg="#ffffff", font=("Arial", 10)).pack(side="left", padx=(0, 5))
        
        self.search_entry = tk.Entry(search_frame, bg="#2d2d2d", fg="#ffffff", insertbackground="white", font=("Arial", 10))
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.filter_playlist)

        self.btn_add = tk.Button(right_panel, text="📁 Add Media Files", command=self.add_files, bg="#007acc", fg="#ffffff", bd=0, padx=10, pady=6, font=("Arial", 10, "bold"))
        self.btn_add.pack(fill="x", pady=(0, 10))

        # Playlist Listbox with Selection Binding
        self.playlist_box = tk.Listbox(
            right_panel, 
            font=("Consolas", 11), 
            bg="#2d2d2d", 
            fg="#00ffcc", 
            selectbackground="#007acc",
            bd=0,
            highlightthickness=0
        )
        self.playlist_box.pack(fill="both", expand=True)
        
        # --- NEW IN DAY 3: Bind Track Selection Event ---
        self.playlist_box.bind("<<ListboxSelect>>", self.on_track_select)

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select Media Files",
            filetypes=(
                ("Media Files", "*.mp3 *.wav *.flac *.aac *.mp4 *.mkv"),
                ("All Files", "*.*")
            )
        )
        if files:
            for file in files:
                if file not in self.playlist:
                    self.playlist.append(file)
            self.update_playlist_box(self.playlist)

    def update_playlist_box(self, items):
        self.playlist_box.delete(0, tk.END)
        self.filtered_list = items
        for item in self.filtered_list:
            self.playlist_box.insert(tk.END, os.path.basename(item))

    def filter_playlist(self, event):
        query = self.search_entry.get().lower()
        if not query:
            self.update_playlist_box(self.playlist)
        else:
            filtered = [s for s in self.playlist if query in os.path.basename(s).lower()]
            self.update_playlist_box(filtered)

    # --- NEW IN DAY 3: Metadata and Album Art Handling ---
    def on_track_select(self, event):
        selection = self.playlist_box.curselection()
        if not selection:
            return
        
        index = selection[0]
        file_path = self.filtered_list[index]
        self.load_metadata_and_art(file_path)

    def load_metadata_and_art(self, file_path):
        art_image = None
        try:
            # Parse tags using Mutagen
            audio = MutagenFile(file_path, easy=False)
            
            # 1. Try extracting EMBEDDED album art (ID3 tags for MP3, FLAC pictures)
            if audio and audio.tags:
                for tag_key in audio.tags.keys():
                    if "APIC" in tag_key or "covr" in tag_key:
                        artwork_data = audio.tags[tag_key].data
                        art_image = Image.open(io.BytesIO(artwork_data))
                        break
            
            # 2. Fallback: Look for a loose 'cover.jpg' file in the same directory
            if not art_image:
                dir_name = os.path.dirname(file_path)
                for filename in ["cover.jpg", "folder.jpg", "album.jpg"]:
                    cover_path = os.path.join(dir_name, filename)
                    if os.path.exists(cover_path):
                        art_image = Image.open(cover_path)
                        break

        except Exception as e:
            print(f"Error loading metadata: {e}")

        # Render image or show fallback placeholder text
        if art_image:
            # Resize image to fit exactly within the 300x240 display frame using high-quality resampling
            art_image = art_image.resize((300, 240), Image.Resampling.LANCZOS)
            self.current_image_ref = ImageTk.PhotoImage(art_image) # Keep reference to prevent garbage collection
            
            self.art_label.config(text="", image=self.current_image_ref)
        else:
            # Fallback text if no art exists anywhere
            self.current_image_ref = None
            self.art_label.config(text=f"🎵\n{os.path.basename(file_path)}", image="")

if __name__ == "__main__":
    root = tk.Tk()
    app = MediaViewer(root)
    root.mainloop()
