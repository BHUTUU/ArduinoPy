import tkinter as tk
from tkinter import filedialog
import vlc

class VideoPlayer(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.media_player = None
        self.media = None
        self.is_fullscreen = False

        # Create GUI elements
        self.create_widgets()

    def create_widgets(self):
        # Create video canvas
        self.video_canvas = tk.Canvas(self, width=640, height=480)
        self.video_canvas.pack()

        # Create control frame
        self.control_frame = tk.Frame(self)
        self.control_frame.pack(pady=10)

        # Create "Open" button
        self.open_button = tk.Button(self.control_frame, text="Open", command=self.open_file)
        self.open_button.pack(side=tk.LEFT, padx=5)

        # Create "Play" button
        self.play_button = tk.Button(self.control_frame, text="Play", command=self.play)
        self.play_button.pack(side=tk.LEFT, padx=5)

        # Create "Pause" button
        self.pause_button = tk.Button(self.control_frame, text="Pause", command=self.pause)
        self.pause_button.pack(side=tk.LEFT, padx=5)

        # Create "Stop" button
        self.stop_button = tk.Button(self.control_frame, text="Stop", command=self.stop)
        self.stop_button.pack(side=tk.LEFT, padx=5)

        # Create volume control
        self.volume_label = tk.Label(self.control_frame, text="Volume:")
        self.volume_label.pack(side=tk.LEFT, padx=5)
        self.volume_scale = tk.Scale(self.control_frame, from_=0, to=100, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_scale.set(50)
        self.volume_scale.pack(side=tk.LEFT, padx=5)

        # Bind mouse movement to show/hide controls
        self.video_canvas.bind("<Motion>", self.toggle_controls)

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4;*.mkv;*.avi")])
        if file_path:
            self.media = vlc.Media(file_path)
            self.media_player = vlc.MediaPlayer()
            self.media_player.set_media(self.media)

            # Set video output to the canvas
            self.media_player.set_hwnd(self.video_canvas.winfo_id())

            # Bind the fullscreen toggle to the canvas
            self.video_canvas.bind("<Double-Button-1>", self.toggle_fullscreen)

    def play(self):
        if self.media_player:
            self.media_player.play()

    def pause(self):
        if self.media_player:
            self.media_player.pause()

    def stop(self):
        if self.media_player:
            self.media_player.stop()

    def set_volume(self, volume):
        if self.media_player:
            self.media_player.audio_set_volume(int(volume))

    def toggle_controls(self, event):
        if self.is_fullscreen:
            if event.x < self.video_canvas.winfo_width() and event.y < self.video_canvas.winfo_height():
                self.control_frame.pack()
            else:
                self.control_frame.pack_forget()

    def toggle_fullscreen(self, event=None):
        self.is_fullscreen = not self.is_fullscreen
        self.master.attributes("-fullscreen", self.is_fullscreen)
        self.video_canvas.focus_set()

        if self.is_fullscreen:
            self.video_canvas.bind("<Escape>", self.toggle_fullscreen)
            self.control_frame.pack_forget()
        else:
            self.video_canvas.unbind("<Escape>")
            self.control_frame.pack()

# Create the main application window
root = tk.Tk()
root.title("Video Player")
root.geometry("800x600")

# Create an instance of the VideoPlayer class
player = VideoPlayer(root)
player.pack(fill=tk.BOTH, expand=True)

# Start the Tkinter event loop
root.mainloop()
