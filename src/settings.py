import json

class Settings:
    def __init__(self):
        self.work_duration = 25  # in minutes
        self.break_duration = 5   # in minutes
        import os
        # Default: Pomodoro folder in user's AppData/Roaming
        appdata = os.environ.get('APPDATA') or os.path.expanduser('~/.config')
        pomodoro_dir = os.path.join(appdata, "Pomodoro")
        if not os.path.exists(pomodoro_dir):
            try:
                os.makedirs(pomodoro_dir, exist_ok=True)
            except Exception:
                pass
        self.goal_save_dir = pomodoro_dir
        self.break_music_file = "Break_Music.mp3"
        self.end_music_file = "End_Music.mp3"
        self.load_settings()

    def load_settings(self):
        try:
            import os
            with open('settings.json', 'r') as f:
                settings = json.load(f)
                self.work_duration = settings.get('work_duration', self.work_duration)
                self.break_duration = settings.get('break_duration', self.break_duration)
                # If goal_save_dir is not set or not in AppData/Pomodoro, update it
                appdata = os.environ.get('APPDATA') or os.path.expanduser('~/.config')
                pomodoro_dir = os.path.join(appdata, "Pomodoro")
                goal_dir = settings.get('goal_save_dir', pomodoro_dir)
                if not goal_dir or not goal_dir.startswith(appdata):
                    goal_dir = pomodoro_dir
                if not os.path.exists(goal_dir):
                    try:
                        os.makedirs(goal_dir, exist_ok=True)
                    except Exception:
                        pass
                self.goal_save_dir = goal_dir
                self.break_music_file = settings.get('break_music_file', self.break_music_file)
                self.end_music_file = settings.get('end_music_file', self.end_music_file)
        except FileNotFoundError:
            self.save_settings()

    def save_settings(self):
        settings = {
            'work_duration': self.work_duration,
            'break_duration': self.break_duration,
            'goal_save_dir': self.goal_save_dir
        }
        settings.update({
            'break_music_file': self.break_music_file,
            'end_music_file': self.end_music_file
        })
        with open('settings.json', 'w') as f:
            json.dump(settings, f)
    
    def get(self, key):
        return getattr(self, key, None)

    def set_work_duration(self, minutes):
        self.work_duration = minutes
        self.save_settings()

    def set_break_duration(self, minutes):
        self.break_duration = minutes
        self.save_settings()