import os
import time
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileHandler(FileSystemEventHandler):
    def __init__(self, src_dir, dest_dir):
        self.src_dir = src_dir
        self.dest_dir = dest_dir

    def on_created(self, event):
        if event.is_directory:
            return

        src_path = event.src_path
        file_name = os.path.basename(src_path)
        dest_path = os.path.join(self.dest_dir, file_name)

        initial_size = os.path.getsize(src_path)
        time.sleep(3)

        if os.path.exists(src_path) and os.path.getsize(src_path) == initial_size:
            try:
                shutil.copy2(src_path, dest_path)
                print(f"Copied: {file_name} to {dest_path}")
            except Exception as e:
                print(f"Error copying {file_name}: {e}")
        else:
            print(f"File download incomplete: {file_name}")

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
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()


