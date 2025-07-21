from tkinter import Tk, Label, Button, Text, StringVar
from timer import Timer
from settings import Settings
from tkinter import Frame
import csv
from datetime import datetime
import os
import threading

class UserInterface:
    def __init__(self, master):
        self.master = master
        # Remove title bar from main window
        self.master.overrideredirect(True)
        self.master.geometry("200x215+{0}+{1}".format(master.winfo_screenwidth() - 220, master.winfo_screenheight() - 270))
        self.master.attributes("-topmost", True)
        self.master.configure(bg="#111111")
        # Add orange border using a Frame
        border_frame = Frame(self.master, bg="#f75828", bd=0, highlightthickness=0)
        border_frame.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.98)
        border_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        # Place the main content inside an inner frame with padding for the border
        content_frame = Frame(border_frame, bg="#111111")
        content_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)
        self.content_frame = content_frame

        self.settings = Settings()
        self.timer = Timer(work_duration=self.settings.work_duration, break_duration=self.settings.break_duration)
        self.time_var = StringVar()
        self.time_var.set(f"{self.settings.work_duration:02}:00")
        
        # Add logo with image and text on top
        from tkinter import PhotoImage
        import sys
        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS
            except AttributeError:
                base_path = os.path.dirname(os.path.abspath(__file__))
            return os.path.join(base_path, relative_path)

        try:
            img_path = resource_path(os.path.join("resources", "pomodoro.png"))
            pomodoro_img = PhotoImage(file=img_path)
            # Resize the image to fit inside 50x50 using subsample if needed
            img_width = pomodoro_img.width()
            img_height = pomodoro_img.height()
            scale_w = max(1, img_width // 25)
            scale_h = max(1, img_height // 25)
            scale = max(scale_w, scale_h)
            if scale > 1:
                pomodoro_img = pomodoro_img.subsample(scale, scale)
            logo_label = Label(content_frame, image=pomodoro_img, text=" Pomodoro", compound="left", font=("Helvetica", 15, "bold"), bg="#111111", fg="#f75828")
            logo_label.image = pomodoro_img  # Keep a reference to avoid garbage collection
        except Exception:
            logo_label = Label(content_frame, text="Pomodoro", font=("Helvetica", 18, "bold"), bg="#111111", fg="#f75828")
        logo_label.pack(pady=(8, 2))

        self.label = Label(content_frame, textvariable=self.time_var, font=("Helvetica", 36), bg="#111111", fg="#ffffff")
        self.label.configure(highlightbackground="#444444", highlightcolor="#444444", bd=0, padx=10, pady=2)
        self.label.pack()

        self.button_frame = Frame(content_frame, bg="#111111")
        self.button_frame.configure(highlightbackground="#444444", highlightcolor="#444444", bd=0, padx=0, pady=2)
        self.button_frame.pack()

        self.start_button = Button(self.button_frame, text="▶", command=self.start_timer,
            width=2,
            height=1,
            font=("Helvetica", 16, "bold"),
            relief="flat",
            bg="#f75828",
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            padx=25,
            pady=2)
        self.start_button.configure(
            highlightbackground="#f0673e",
            highlightcolor="#444444",
            borderwidth=2
        )
        self.start_button.pack(side="left", padx=5)

        self.reset_button = Button(
            self.button_frame,
            text="⟲",
            command=self.reset_timer,
            width=2,
            height=1,
            font=("Helvetica", 16, "bold"),
            relief="flat",
            bg="#222222",
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            padx=2,
            pady=2
        )
        self.reset_button.configure(
            highlightbackground="#444444",
            highlightcolor="#444444",
            borderwidth=2
        )
        self.reset_button.pack(side="left", padx=5)

        # Add the settings button with a gear icon (Unicode ⚙)
        self.settings_button = Button(
            self.button_frame,
            text="⚙",  # Unicode gear icon
            command=self.open_settings,
            width=2,
            height=1,
            font=("Helvetica", 12, "bold"),
            relief="flat",
            bg="#333333",
            fg="#ffffff",
            bd=0,
            highlightthickness=0,
            padx=5,
            pady=5
        )
        self.settings_button.configure(
            highlightbackground="#444444",
            highlightcolor="#444444",
            borderwidth=2
        )
        self.settings_button.pack(side="left", padx=5)

        # Make the goals_text the same width as the button_frame
        self.goals_text = Text(
            content_frame,
            height=2,
            width=1,  # Will be overridden by 'pack'
            bd=0,
            highlightthickness=0,
            relief="flat",
            bg="#222222",
            fg="#ffffff",
            wrap="word",
        )
        self.goals_text.configure(
            padx=8,
            pady=4,
            font=("Helvetica", 10),
            insertbackground="#ffffff"
        )
        # Use 'fill="x"' and same padx as button_frame for width alignment
        self.goals_text.pack(pady=(10, 0), fill="x", padx=10)

        # Overlay label for break
        self.break_overlay = None

        # Add floating close button on top right
        close_button = Button(self.master, text="✕", command=self.master.destroy,
                              font=("Helvetica", 8, "bold"), bg="#111111", fg="#f75828", bd=0, padx=3 , pady=3,
                              relief="flat", highlightthickness=0, activebackground="#d32f2f", activeforeground="#f75828")
        close_button.place(relx=1.0, x=-4, y=4, anchor="ne", width=16, height=16)

    def play_sound(self, music_file=None):
        # Play the given music file from resources folder, fallback to system sound
        import sys
        def resource_path(relative_path):
            try:
                base_path = sys._MEIPASS
            except AttributeError:
                base_path = os.path.abspath(".")
            return os.path.join(base_path, relative_path)

        if music_file is None:
            music_file = self.settings.break_music_file  # fallback
        try:
            import pygame
            pygame.mixer.init()
            music_path = resource_path(os.path.join("resources", music_file))
            pygame.mixer.music.load(music_path)
            pygame.mixer.music.play()
        except Exception as e:
            try:
                import winsound
                winsound.PlaySound("SystemExclamation", winsound.SND_ALIAS)
            except Exception:
                pass

    def update_timer_display(self):
        self.time_var.set(self.timer.get_time())
        # Show overlay if in break, hide if not
        if self.timer.is_break:
            if not self.break_overlay:
                # Create overlay label covering goals_text and button_frame
                self.break_overlay = Label(self.content_frame, text="BREAK", font=("Helvetica", 22, "bold"),
                                          bg="#f75828", fg="#fff", bd=0, relief="flat")
                # Place overlay over goals_text and button_frame
                self.break_overlay.place(relx=0, rely=0.48, relwidth=1, relheight=0.52)
        else:
            if self.break_overlay:
                self.break_overlay.destroy()
                self.break_overlay = None

        if self.timer.is_timer_running():
            self.timer.tick()  # Decrement the timer
            if self.timer.remaining_time == 0:
                if not self.timer.is_break:
                    # Work session ended, play break music and start break
                    threading.Thread(target=self.play_sound, args=(self.settings.break_music_file,), daemon=True).start()
                    self.timer.is_break = True
                    self.timer.remaining_time = self.settings.break_duration * 60
                    self.update_timer_display()
                    return
                else:
                    # Break ended, play end music and stop timer
                    threading.Thread(target=self.play_sound, args=(self.settings.end_music_file,), daemon=True).start()
                    self.timer.is_running = False
                    self.timer.is_break = False
                    self.time_var.set("00:00")
                    # Remove overlay if present
                    if self.break_overlay:
                        self.break_overlay.destroy()
                        self.break_overlay = None
                    return
            self.master.after(1000, self.update_timer_display)

    def reset_timer(self):
        self.timer.reset()
        self.goals_text.delete("1.0", "end")  # Clear the goal text box
        self.update_timer_display()
        
    def start_timer(self):
        # Always start a work session, not a break
        self.timer.is_break = False
        self.timer.is_running = False
        self.timer.remaining_time = self.settings.work_duration * 60
        self.timer.start()
        goal_text = self.goals_text.get("1.0", "end").strip()
        save_dir = self.settings.get("goal_save_dir")
        if save_dir and goal_text:
            os.makedirs(save_dir, exist_ok=True)
            file_path = os.path.join(save_dir, "goals.csv")
            file_exists = os.path.isfile(file_path)
            with open(file_path, mode="a", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile)
                if not file_exists:
                    writer.writerow(["TimeStamp", "Goal", "Work Duration (min)"])
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    goal_text,
                    self.settings.work_duration
                ])
        self.goals_text.focus_set()
        self.master.focus()
        self.update_timer_display()

    def open_settings(self):
        # Disable the settings button if popup is already open
        if hasattr(self, '_settings_popup_open') and self._settings_popup_open:
            return
        self._settings_popup_open = True
        self.settings_button.config(state="disabled")
        # Create a popup window
        settings_popup = Tk()
        settings_popup.overrideredirect(True)
        settings_popup.attributes("-topmost", True)
        settings_popup.title("Settings")
        settings_popup.geometry("300x300")
        settings_popup.configure(bg="#222222")
        # Add orange border using a Frame
        border_frame = Frame(settings_popup, bg="#000", bd=0, highlightthickness=0)
        border_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        # Place the popup content inside an inner frame with padding for the border
        content_frame = Frame(border_frame, bg="#222222")
        content_frame.place(relx=0.02, rely=0.02, relwidth=0.96, relheight=0.96)

        # Position the popup right above the master window
        self.master.update_idletasks()
        master = self.master
        master_x = self.master.winfo_x()
        master_y = self.master.winfo_y()
        master_width = self.master.winfo_width()
        popup_width = 300
        popup_height = 350
        popup_x = master_x + (master_width // 2) - (popup_width // 2)
        popup_y = max(0, master_y - popup_height - 10)
        settings_popup.geometry("300x350+{0}+{1}".format(master.winfo_screenwidth() - 320, master.winfo_screenheight() - 630))

        from tkinter import Label, Entry, Button, LEFT, W
        # Add a label at the top for 'Settings'
        settings_title = Label(content_frame, text="Settings", font=("Helvetica", 12, "bold"), bg="#222222", fg="#f75828")
        settings_title.pack(pady=(8, 0))

        # Work duration
        Label(content_frame, text="Work Duration (minutes):", bg="#222222", fg="#ffffff", anchor="w", justify="left").pack(pady=(20, 0), anchor=W, padx=10, fill="x")
        work_entry = Entry(content_frame)
        work_entry.insert(0, str(self.settings.work_duration))
        work_entry.pack(pady=5, anchor=W, padx=10, fill="x")

        # Break duration
        Label(content_frame, text="Break Duration (minutes):", bg="#222222", fg="#ffffff", anchor="w", justify="left").pack(pady=(10, 0), anchor=W, padx=10, fill="x")
        break_entry = Entry(content_frame)
        break_entry.insert(0, str(self.settings.break_duration))
        break_entry.pack(pady=5, anchor=W, padx=10, fill="x")

        # Goal save dir
        Label(content_frame, text="Goal Save Directory:", bg="#222222", fg="#ffffff", anchor="w", justify="left").pack(pady=(10, 0), anchor=W, padx=10, fill="x")
        dir_entry = Entry(content_frame, width=30)
        dir_entry.insert(0, str(self.settings.goal_save_dir))
        dir_entry.pack(pady=5, anchor=W, padx=10, fill="x")

        def open_goals_file():
            import subprocess, sys
            save_dir = dir_entry.get().strip()
            if save_dir:
                file_path = os.path.join(save_dir, "goals.csv")
                if os.path.isfile(file_path):
                    try:
                        os.startfile(file_path)
                    except AttributeError:
                        subprocess.Popen(["open" if sys.platform == "darwin" else "xdg-open", file_path])
                else:
                    import tkinter.messagebox as mb
                    mb.showinfo("File Not Found", f"{file_path} does not exist.")
            else:
                import tkinter.messagebox as mb
                mb.showinfo("No Path", "Goal save directory is empty.")

        open_file_link = Label(content_frame, text="Open File", fg="#2196F3", cursor="hand2", bg="#222222", font=("Helvetica", 10, "underline"))
        open_file_link.pack(anchor=W, padx=10, pady=(0, 10))
        open_file_link.bind("<Button-1>", lambda e: open_goals_file())

        def on_close():
            self._settings_popup_open = False
            self.settings_button.config(state="normal")
            settings_popup.destroy()

        def save_and_close():
            try:
                self.settings.set_work_duration(int(work_entry.get()))
                self.settings.set_break_duration(int(break_entry.get()))
                self.settings.goal_save_dir = dir_entry.get()
                self.settings.save_settings()
                # Reset timer with new settings
                self.timer = Timer(work_duration=self.settings.work_duration, break_duration=self.settings.break_duration)
                self.time_var.set(f"{self.settings.work_duration:02}:00")
                self.update_timer_display()
                on_close()
            except Exception as e:
                import tkinter.messagebox as mb
                mb.showerror("Error", f"Invalid input: {e}")

        def cancel_and_close():
            on_close()

        button_frame_popup = Frame(content_frame, bg="#222222")
        button_frame_popup.pack(pady=15, anchor=W, padx=10, fill="x")
        Button(button_frame_popup, text="Save", command=save_and_close, bg="#f75828", fg="#fff", relief="flat").pack(side="left", padx=(0,10))
        Button(button_frame_popup, text="Cancel", command=cancel_and_close, bg="#444444", fg="#fff", relief="flat").pack(side="left")
        settings_popup.protocol("WM_DELETE_WINDOW", on_close)
        settings_popup.mainloop()

def main():
    root = Tk()
    app = UserInterface(root)
    root.mainloop()

if __name__ == "__main__":
    main()