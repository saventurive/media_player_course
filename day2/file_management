import os
import tkinter as tk
from tkinter import filedialog, ttk

class MediaViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Player - Day 2")
        self.root.geometry("900x560")
        self.root.config(bg="#1e1e1e")

        # --- NEW IN DAY 2: Application State Lists ---
        self.playlist = []
        self.filtered_list = []
        # ---------------------------------------------

        # Top Menu Bar
        menu_bar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open Media...", command=self.add_files)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Preferences", command=lambda: print("Preferences selected"))
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        self.root.config(menu=menu_bar)

        # Left Panel (Display Area & Controls)
        left_panel = tk.Frame(self.root, bg="#1e1e1e")
        left_panel.pack(side="left", fill="both", padx=20, pady=20)

        # Right Panel (Playlist & Search)
        right_panel = tk.Frame(self.root, bg="#1e1e1e")
        right_panel.pack(side="right", fill="both", expand=True, padx=20, pady=20)

        # Display Frame Container
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

        # --- NEW IN DAY 2: Search Bar & Add Media Button ---
        search_frame = tk.Frame(right_panel, bg="#1e1e1e")
        search_frame.pack(fill="x", pady=(0, 8))

        tk.Label(search_frame, text="Search:", bg="#1e1e1e", fg="#ffffff", font=("Arial", 10)).pack(side="left", padx=(0, 5))
        
        self.search_entry = tk.Entry(search_frame, bg="#2d2d2d", fg="#ffffff", insertbackground="white", font=("Arial", 10))
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.filter_playlist)

        self.btn_add = tk.Button(right_panel, text="📁 Add Media Files", command=self.add_files, bg="#007acc", fg="#ffffff", bd=0, padx=10, pady=6, font=("Arial", 10, "bold"))
        self.btn_add.pack(fill="x", pady=(0, 10))
        # ---------------------------------------------------

        # Playlist Listbox
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

    # --- NEW IN DAY 2: File Management Methods ---
    def add_files(self):
        # Expanded file types tuple allowing custom audio/video additions
        files = filedialog.askopenfilenames(
            title="Select Media Files",
            filetypes=(
                ("Media Files", "*.mp3 *.wav *.flac *.aac *.mp4 *.mkv *.avi *.mov *.webm"),
                ("Audio Files", "*.mp3 *.wav *.flac *.aac"),
                ("Video Files", "*.mp4 *.mkv *.avi *.mov *.webm"),
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
    # ---------------------------------------------

if __name__ == "__main__":
    root = tk.Tk()
    app = MediaViewer(root)
    root.mainloop()
