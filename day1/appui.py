import tkinter as tk
from tkinter import ttk

class MediaViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Player - Day 1")
        self.root.geometry("900x560")
        self.root.config(bg="#1e1e1e")

        # Top Menu Bar
        menu_bar = tk.Menu(self.root)
        
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Open Media...", command=lambda: print("Open selected"))
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

        # Display Frame Container (Where Album Art or Video will eventually live)
        self.display_frame = tk.Frame(left_panel, bg="#2d2d2d", width=300, height=240)
        self.display_frame.pack(pady=(0, 15))
        self.display_frame.pack_propagate(False) # Prevents frame from shrinking

        # Styled Label with Custom Font and Colors
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

        # Control Buttons Container with Styled Colors
        btn_frame = tk.Frame(left_panel, bg="#1e1e1e")
        btn_frame.pack()
        
        btn_styles = {"bg": "#333333", "fg": "#ffffff", "bd": 0, "padx": 10, "pady": 6, "font": ("Arial", 10)}
        for text in ["⏮ Prev", "▶ Play", "⏹ Stop", "⏭ Next"]:
            tk.Button(btn_frame, text=text, **btn_styles).pack(side="left", padx=4)

        # Playlist Listbox with Custom Aesthetics
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

if __name__ == "__main__":
    root = tk.Tk()
    app = MediaViewer(root)
    root.mainloop()
