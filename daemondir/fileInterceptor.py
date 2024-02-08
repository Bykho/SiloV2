import os
import shutil
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json
import subprocess  # Import subprocess module
from classifier import run_classification  # Import the run_classification function


# Define the global variable for the data.json file path
DATA_FILE = os.path.join(os.path.expanduser("~/Desktop/SiloV2"), "data.json")

class FileHandler(FileSystemEventHandler):
    def __init__(self, src_dir, dest_dir, data_file):
        self.src_dir = src_dir
        self.dest_dir = dest_dir

        # Initialize data file with an empty list if it doesn't exist or empty
        if not os.path.exists(DATA_FILE) or os.path.getsize(DATA_FILE) == 0:
            with open(DATA_FILE, 'w') as f:
                json.dump([], f)
    
        print(data_file)

    def on_created(self, event):
        if event.is_directory:
            return
        print('check if on_created works')
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
        
            # Update data.json file
            self.update_data_file(file_name)

            # After moving the file, classify it
            classification_result = run_classification(dest_path)
            print(f"Classification Result for {file_name}: {classification_result}")
        except Exception as e:
            print(f"Error moving {file_name}: {e}")

    def on_deleted(self, event):
        if event.is_directory:
            return
        print('check if on_deleted works')
        src_path = event.src_path

        # Check if the file still exists at src_path
        if not os.path.exists(src_path):
            print(f"File {src_path} no longer exists.")
            return

        file_name = os.path.basename(src_path)
        dest_path = os.path.join(self.dest_dir, file_name)

        try:
            os.remove(dest_path)
            print(f"Deleted: {file_name}")

            # Update data.json file
            #self.remove_from_data_file(file_name)
        except Exception as e:
            print(f"Error deleting {file_name}: {e}")

    def update_data_file(self, file_name):
        data = []
        try:
            if os.path.exists(DATA_FILE):
                with open(DATA_FILE, 'r') as f:
                    data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
        if file_name not in data:
            data.append(file_name)
        try:
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print("An error occurred while dumping:", e)

    def remove_from_data_file(self, file_name):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r') as f:
                data = json.load(f)
                if file_name in data:
                    data.remove(file_name)
            
            with open(DATA_FILE, 'w') as f:
                json.dump(data, f, indent=4)

def main():
    desktop_dir = os.path.expanduser("~/Desktop")
    copied_file_folder = os.path.join(desktop_dir, "SiloV2/SH")
    data_file = os.path.join(desktop_dir, "SiloV2", "data.json")

    if not os.path.exists(copied_file_folder):
        os.mkdir(copied_file_folder)

    event_handler = FileHandler(desktop_dir, copied_file_folder, data_file)
    observer = Observer()
    observer.schedule(event_handler, path=desktop_dir, recursive=False)
    observer.start()

    try:
        display_process = subprocess.Popen(["python3", os.path.join(os.path.dirname(__file__), "display.py")])

        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    main()





