# Pomodoro Timer App

This is a simple Pomodoro timer application designed to help users manage their time effectively using the Pomodoro technique. The application features a floating timer window that allows users to focus on their tasks while keeping track of work and break intervals.

## PyInstaller build query
(.venv) C:\Users\Gowtham Raj\Documents\LLM\Commander\Pomo\pomodoro-timer-app>.venv\Scripts\python.exe -m PyInstaller --onefile --noconsole --strip --clean --add-data "src/resources;resources" --icon=src/resources/pomodoro.ico --exclude-module test --exclude-module tkinter.test src/Pomodoro.py

## Features

- 25-minute work timer with a 5-minute break
- Floating window positioned in the bottom right corner of the screen
- Reset button to restart the timer
- Text area for setting and tracking goals
- Settings button to customize timer durations and preferences

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   ```
2. Navigate to the project directory:
   ```
   cd pomodoro-timer-app
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
python src/main.py
```

Once the application is running, you can start the timer, take breaks, and reset the timer as needed. Use the text area to jot down your goals for the session.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.