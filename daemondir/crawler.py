import os
from SiloV2.CA import classify  # Import the classify function

def classify_directory(directory_path):
    # Recursively scan the specified directory and its children
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                # Apply the 'classify' function to each file
                result = classify(file_path)
                print(f"Classified {file}: {result}")
            except Exception as e:
                print(f"Error classifying {file}: {e}")

if __name__ == "__main__":
    target_directory = "~/Desktop"  # Replace with your target directory path
    classify_directory(target_directory)


