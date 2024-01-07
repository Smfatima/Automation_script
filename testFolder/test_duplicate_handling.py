import unittest
import os
import shutil
import tempfile
from main import organize_files

class TestDuplicateHandling(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def test_duplicate_handling(self):
        # Test how the script handles duplicate files
        source_folder = os.path.join(self.test_dir, "source_folder")
        target_folder = os.path.join(self.test_dir, "target_folder")
        os.makedirs(source_folder, exist_ok=True)
        os.makedirs(target_folder, exist_ok=True)

        # Create two files with the same name in the source folder
        duplicate_file = os.path.join(source_folder, "duplicate_file.txt")
        with open(duplicate_file, "w") as f:
            f.write("This is a duplicate file.")

        categories = {
            "text_files": (".txt",),
        }
        duplicate_action = "overwrite"

        # Organize files with duplicate_action set to "overwrite"
        result = organize_files(source_folder, target_folder, categories, duplicate_action)

        # Ensure that only one file exists in the target folder
        target_files = os.listdir(os.path.join(target_folder, "text_files"))
        self.assertEqual(len(target_files), 1)

        # Ensure that the result is True (successful)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
