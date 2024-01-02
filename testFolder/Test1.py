# Test script for duplicate handling

def test_duplicate_handling(self):
    source_folder = os.path.join(self.test_dir, "source_folder")
    target_folder = os.path.join(self.test_dir, "target_folder")
    os.makedirs(source_folder, exist_ok=True)
    os.makedirs(target_folder, exist_ok=True)

    # Create two files with the same name in the source folder
    file1 = os.path.join(source_folder, "duplicate_file.txt")
    file2 = os.path.join(source_folder, "duplicate_file.txt")
    with open(file1, "w") as f1, open(file2, "w") as f2:
        f1.write("File content")
        f2.write("File content")

    categories = {
        "text_files": (".txt",),
    }
    duplicate_action = "overwrite"

    result = organize_files(source_folder, target_folder, categories, duplicate_action)

    # Ensure that only one file exists in the target folder
    target_files = os.listdir(os.path.join(target_folder, "text_files"))
    self.assertEqual(len(target_files), 1)

    # Ensure that the result is True (successful)
    self.assertTrue(result)
