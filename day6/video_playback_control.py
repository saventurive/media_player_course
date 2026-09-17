import os
import io
import tkinter as tk
from tkinter import filedialog, ttk
from mutagen import File as MutagenFile
from PIL import Image, ImageTk
import vlc

class MediaViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Player - Day 6 (Video & Audio)")
        self.root.geometry("950x600")
        self.root.config(bg="#1e1e1e")

        # --- NEW IN DAY 6: Initialize VLC Instance ---
        self.vlc_instance = vlc.Instance()
        self.vlc_player = self.vlc_instance.media_player_new()

        # Application State
        self.playlist = []
        self.filtered_list = []
        self.current_image_ref = None
        self.is_playing = False
        self.current_track_duration = 0.0

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

        # Display Frame Container (Acts as both Album Art container and VLC Video Canvas)
        self.display_frame = tk.Frame(left_panel, bg="#2d2d2d", width=360, height=240)
        self.display_frame.pack(pady=(0, 15))
        self.display_frame.pack_propagate(False)

        self.art_label = tk.Label(
            self.display_frame, 
            text="🎬🎵\nNo Media Loaded", 
            font=("Arial", 14, "bold"), 
            bg="#2d2d2d", 
            fg="#aaaaaa"
        )
        self.art_label.pack(fill="both", expand=True)

        # Time Display & Progress Slider
        slider_frame = tk.Frame(left_panel, bg="#1e1e1e")
        slider_frame.pack(fill="x", pady=(0, 5))
        
        self.time_label = tk.Label(slider_frame, text="00:00 / 00:00", bg="#1e1e1e", fg="#aaaaaa", font=("Consolas", 9))
        self.time_label.pack(side="right")

        self.progress_slider = ttk.Scale(left_panel, from_=0, to=100, orient="horizontal", command=self.on_seek)
        self.progress_slider.pack(fill="x", pady=(0, 10))

        # Speed Control Selector
        speed_frame = tk.Frame(left_panel, bg="#1e1e1e")
        speed_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(speed_frame, text="Speed:", bg="#1e1e1e", fg="#ffffff", font=("Arial", 9)).pack(side="left", padx=(0, 5))
        self.speed_combobox = ttk.Combobox(speed_frame, values=["0.5x", "0.75x", "1.0x", "1.25x", "1.5x", "2.0x"], width=8, state="readonly")
        self.speed_combobox.set("1.0x")
        self.speed_combobox.pack(side="left")
        self.speed_combobox.bind("<<ComboboxSelected>>", self.change_speed)

        # Control Buttons Container
        btn_frame = tk.Frame(left_panel, bg="#1e1e1e")
        btn_frame.pack()
        
        btn_styles = {"bg": "#333333", "fg": "#ffffff", "bd": 0, "padx": 8, "pady": 6, "font": ("Arial", 9)}
        
        tk.Button(btn_frame, text="⏪ -5s", command=lambda: self.skip_time(-5), **btn_styles).pack(side="left", padx=2)
        tk.Button(btn_frame, text="▶ Play", command=self.play_media, **btn_styles).pack(side="left", padx=2)
        tk.Button(btn_frame, text="⏹ Stop", command=self.stop_media, **btn_styles).pack(side="left", padx=2)
        tk.Button(btn_frame, text="⏩ +5s", command=lambda: self.skip_time(5), **btn_styles).pack(side="left", padx=2)

        # Search Bar & Add Media Button
        search_frame = tk.Frame(right_panel, bg="#1e1e1e")
        search_frame.pack(fill="x", pady=(0, 8))

        tk.Label(search_frame, text="Search:", bg="#1e1e1e", fg="#ffffff", font=("Arial", 10)).pack(side="left", padx=(0, 5))
        
        self.search_entry = tk.Entry(search_frame, bg="#2d2d2d", fg="#ffffff", insertbackground="white", font=("Arial", 10))
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.bind("<KeyRelease>", self.filter_playlist)

        self.btn_add = tk.Button(right_panel, text="📁 Add Media Files", command=self.add_files, bg="#007acc", fg="#ffffff", bd=0, padx=10, pady=6, font=("Arial", 10, "bold"))
        self.btn_add.pack(fill="x", pady=(0, 10))

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
        self.playlist_box.bind("<<ListboxSelect>>", self.on_track_select)

        # Start UI update loop
        self.update_progress_loop()

    def format_time(self, seconds):
        if not seconds or seconds < 0:
            return "00:00"
        mins = int(seconds // 60)
        secs = int(seconds % 60)
        return f"{mins:02d}:{secs:02d}"

    def update_progress_loop(self):
        if self.is_playing:
            current_ms = self.vlc_player.get_time()
            if current_ms >= 0:
                current_sec = current_ms / 1000.0
                self.progress_slider.config(to=self.current_track_duration)
                self.progress_slider.set(current_sec)
                
                time_str = f"{self.format_time(current_sec)} / {self.format_time(self.current_track_duration)}"
                self.time_label.config(text=time_str)
                
        self.root.after(1000, self.update_progress_loop)

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="Select Media Files",
            filetypes=(
                ("All Media Files", "*.mp3 *.wav *.flac *.aac *.mp4 *.mkv *.avi"),
                ("Audio Files", "*.mp3 *.wav *.flac *.aac"),
                ("Video Files", "*.mp4 *.mkv *.avi"),
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

    def on_track_select(self, event):
        selection = self.playlist_box.curselection()
        if not selection:
            return
        index = selection[0]
        file_path = self.filtered_list[index]
        
        # Determine duration using VLC media descriptor or Mutagen fallback
        ext = os.path.splitext(file_path)[1].lower()
        if ext in ['.mp4', '.mkv', '.avi']:
            media = self.vlc_instance.media_new(file_path)
            media.parse()
            self.current_track_duration = media.get_duration() / 1000.0
        else:
            try:
                audio_info = MutagenFile(file_path)
                self.current_track_duration = audio_info.info.length if audio_info and audio_info.info else 0.0
            except Exception:
                self.current_track_duration = 0.0

        self.load_media_display(file_path)

    def load_media_display(self, file_path):
        ext = os.path.splitext(file_path)[1].lower()
        is_video = ext in ['.mp4', '.mkv', '.avi']

        if is_video:
            # Hide text label, clear image, prepare frame for VLC rendering
            self.art_label.config(text="", image="")
            # Bind VLC output to our Tkinter display frame window handle
            if os.name == 'nt': # Windows
                self.vlc_player.set_hwnd(self.display_frame.winfo_id())
            else: # Linux / macOS XID
                self.vlc_player.set_xwindow(self.display_frame.winfo_id())
        else:
            # Handle audio and album art loading
            self.vlc_player.stop()
            art_image = None
            try:
                audio = MutagenFile(file_path, easy=False)
                if audio and audio.tags:
                    for tag_key in audio.tags.keys():
                        if "APIC" in tag_key or "covr" in tag_key:
                            artwork_data = audio.tags[tag_key].data
                            art_image = Image.open(io.BytesIO(artwork_data))
                            break
                if not art_image:
                    dir_name = os.path.dirname(file_path)
                    for filename in ["cover.jpg", "folder.jpg", "album.jpg"]:
                        cover_path = os.path.join(dir_name, filename)
                        if os.path.exists(cover_path):
                            art_image = Image.open(cover_path)
                            break
            except Exception as e:
                print(f"Metadata error: {e}")

            if art_image:
                art_image = art_image.resize((360, 240), Image.Resampling.LANCZOS)
                self.current_image_ref = ImageTk.PhotoImage(art_image)
                self.art_label.config(text="", image=self.current_image_ref)
            else:
                self.current_image_ref = None
                self.art_label.config(text=f"🎵\n{os.path.basename(file_path)}", image="")

    def play_media(self):
        selection = self.playlist_box.curselection()
        if not selection:
            return
        file_path = self.filtered_list[selection[0]]
        
        media = self.vlc_instance.media_new(file_path)
        self.vlc_player.set_media(media)
        
        # Re-attach window handle for video streams just in case
        if os.path.splitext(file_path)[1].lower() in ['.mp4', '.mkv', '.avi']:
            if os.name == 'nt':
                self.vlc_player.set_hwnd(self.display_frame.winfo_id())
            else:
                self.vlc_player.set_xwindow(self.display_frame.winfo_id())

        self.vlc_player.play()
        self.is_playing = True

    def stop_media(self):
        self.vlc_player.stop()
        self.is_playing = False
        self.time_label.config(text="00:00 / " + self.format_time(self.current_track_duration))
        self.progress_slider.set(0)

    def skip_time(self, seconds_delta):
        if not self.is_playing:
            return
        current_ms = self.vlc_player.get_time()
        new_ms = max(0, current_ms + int(seconds_delta * 1000))
        self.vlc_player.set_time(new_ms)

    def on_seek(self, value):
        # Triggered when user interacts with the progress slider
        if self.is_playing:
            target_sec = float(value)
            # Only seek if user is actively dragging near target
            current_sec = self.vlc_player.get_time() / 1000.0
            if abs(target_sec - current_sec) > 1.5:
                self.vlc_player.set_time(int(target_sec * 1000))

    def change_speed(self, event):
        speed_str = self.speed_combobox.get()
        speed_val = float(speed_str.replace("x", ""))
        self.vlc_player.set_rate(speed_val)
        print(f"Playback speed changed to {speed_val}x")

if __name__ == "__main__":
    root = tk.Tk()
    app = MediaViewer(root)
    root.mainloop()
