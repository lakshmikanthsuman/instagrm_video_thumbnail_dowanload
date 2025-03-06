import os
import shutil

def rename_files(source_folder, destination_folder):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    for filename in os.listdir(source_folder):
        old_path = os.path.join(source_folder, filename)
        if os.path.isfile(old_path):  # Ensure it's a file
            new_filename = filename.lower().replace(" ", "_")
            new_path = os.path.join(destination_folder, new_filename)
            shutil.copy2(old_path, new_path)  # Copy with metadata
            print(f'Renamed: {filename} -> {new_filename}')

source_folder = r"C:\Users\HP\Downloads\new finone\files dowanloaded\feb 16-27\IG\videos\compressed"
destination_folder = r"C:\Users\HP\Downloads\new finone\files dowanloaded\feb 16-27\IG\videos\compressed\renamed"

rename_files(source_folder, destination_folder)