# The main script for organizing the download folder

import os
import shutil
import concurrent.futures
import argparse
import logging
import gettext  # Import the gettext module
from tqdm import tqdm

# Configure localization (i18n)
gettext.install('organize_files', localedir='locales')

def create_folders(target_folder, folder_names):
    try:
        for folder_name in folder_names:
            folder_path = os.path.join(target_folder, folder_name)
            os.makedirs(folder_path, exist_ok=True)
    except OSError as e:
        logging.error(_("Error creating folders: {0}").format(str(e)))
        print(_("Error creating folders: {0}").format(str(e)))
        return False

    return True

def organize_file(file_path, target_folder, categories, duplicate_action):
    _, file_extension = os.path.splitext(file_path)

    # Determine the category for the file based on its extension
    file_category = None
    for category, extensions in categories.items():
        if file_extension.lower() in extensions:
            file_category = category
            break

    if file_category is None:
        # If the file doesn't match any category, organize it by extension
        file_category = file_extension[1:]  # Remove the leading dot from the extension

    category_folder = os.path.join(target_folder, file_category)

    # Handle duplicate file names
    destination_path = os.path.join(category_folder, os.path.basename(file_path))
    if os.path.exists(destination_path):
        if duplicate_action == "overwrite":
            os.remove(destination_path)
        elif duplicate_action == "rename":
            index = 1
            base, ext = os.path.splitext(destination_path)
            while os.path.exists(destination_path):
                destination_path = f"{base}_{index}{ext}"
                index += 1
        else:
            return

    # Ensure the category folder exists
    os.makedirs(category_folder, exist_ok=True)

    try:
        shutil.move(file_path, destination_path)
        print(_("Moved {0} to {1}").format(file_path, destination_path))
    except (shutil.Error, IOError) as e:
        logging.error(_("Failed to move {0} to {1}: {2}").format(file_path, destination_path, str(e)))
        print(_("Failed to move {0} to {1}: {2}").format(file_path, destination_path, str(e)))

def organize_files(source_folder, target_folder, categories, duplicate_action):
    _ = gettext.gettext  # Associate _ with the translation function

    # Check if the source folder exists
    if not os.path.exists(source_folder):
        logging.error(_("The source folder '{0}' does not exist.").format(source_folder))
        print(_("The source folder '{0}' does not exist.").format(source_folder))
        return False

    # Check if the target folder exists; create it if it doesn't
    os.makedirs(target_folder, exist_ok=True)

    # Create folders for each category and their associated sub-folders
    if not create_folders(target_folder, categories.keys()):
        return False

    for category, sub_folders in categories.items():
        category_folder = os.path.join(target_folder, category)
        create_folders(category_folder, sub_folders)

    # List all files in the source folder (including subdirectories)
    file_list = []
    for root, _, files in os.walk(source_folder):
        for filename in files:
            file_list.append(os.path.join(root, filename))

    # Organize files in parallel with a progress indicator
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = []
        for file_path in file_list:
            futures.append(executor.submit(organize_file, file_path, target_folder, categories, duplicate_action))

        # Display a progress bar for file organization
        for _ in tqdm(concurrent.futures.as_completed(futures), total=len(futures), unit="file"):
            pass

    return True

def main():
    parser = argparse.ArgumentParser(description=_("Organize files into categorized folders."))
    parser.add_argument('source_folder', help=_("Specify the source folder path where files are organized from."))
    parser.add_argument('target_folder', help=_("Specify the target folder path where files are organized into."))
    parser.add_argument('-d', '--duplicate-action', choices=['overwrite', 'rename', 'skip'],
                        default='skip', help=_("Specify the action to take on duplicate files (default: skip)."))
    parser.add_argument('-l', '--log', help=_("Specify the path to the log file."))
    args = parser.parse_args()

    # Define categories and their associated sub-folders
    categories = {
        "word_files": (".docx", ".doc"),
        "video_files": (".mkv", ".mp4", ".webm"),
        "image_files": (".jpg", ".jpeg", ".png", ".gif", ".bmp"),
        "pdf_files": (".pdf"),
        "zip_files": (".zip", ".rar", ".7z"),
    }

    # Initialize logging
    if args.log:
        logging.basicConfig(filename=args.log, level=logging.INFO)

    # Attempt to organize files
    if organize_files(args.source_folder, args.target_folder, categories, args.duplicate_action):
        print(_("Files organized successfully!"))
    else:
        print(_("File organization unsuccessful. Please check the source and target folder paths."))

if __name__ == "__main__":
    main()
