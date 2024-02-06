import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess  # Import subprocess module

class FileHandler(FileSystemEventHandler):
    def __init__(self, src_dir, dest_dir):
        self.src_dir = src_dir
        self.dest_dir = dest_dir

    def on_created(self, event):
        if event.is_directory:
            return

        src_path = event.src_path

        # Check if the file still exists at src_path
        if not os.path.exists(src_path):
            print(f"File {src_path} no longer exists.")
            return

        file_name = os.path.basename(src_path)
        dest_path = os.path.join(self.dest_dir, file_name)

        try:
            shutil.move(src_path, dest_path)
            print(f"Moved: {file_name} to {dest_path}")
        except Exception as e:
            print(f"Error moving {file_name}: {e}")

def main():
    desktop_dir = os.path.expanduser("~/Desktop")
    copied_file_folder = os.path.join(desktop_dir, "SiloV2/SH")

    if not os.path.exists(copied_file_folder):
        os.mkdir(copied_file_folder)

    event_handler = FileHandler(desktop_dir, copied_file_folder)
    observer = Observer()
    observer.schedule(event_handler, path=desktop_dir, recursive=False)
    observer.start()

    try:

        display_process = subprocess.Popen(["python3", "display.py"])


        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()




