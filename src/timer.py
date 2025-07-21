class Timer:
    def __init__(self, work_duration=25, break_duration=5):
        self.work_duration = work_duration * 60  # Convert to seconds
        self.break_duration = break_duration * 60  # Convert to seconds
        self.remaining_time = self.work_duration
        self.is_running = False
        self.is_break = False

    def start(self):
        self.is_running = True

    def pause(self):
        self.is_running = False

    def reset(self):
        self.remaining_time = self.work_duration
        self.is_running = False
        self.is_break = False

    def tick(self):
        if self.is_running:
            if self.remaining_time > 0:
                self.remaining_time -= 1
            else:
                self.is_break = not self.is_break
                self.remaining_time = self.break_duration if self.is_break else self.work_duration

    def get_time(self):
        minutes, seconds = divmod(self.remaining_time, 60)
        return f"{minutes:02}:{seconds:02}"

    def is_timer_running(self):
        return self.is_running

    def is_on_break(self):
        return self.is_break