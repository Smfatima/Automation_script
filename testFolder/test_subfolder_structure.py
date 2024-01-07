import unittest
import os
import shutil
import tempfile
from main import organize_files

class TestSubFolderStructure(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory for testing
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        # Clean up the temporary directory
        shutil.rmtree(self.test_dir)

    def test_subfolder_structure(self):
        # Test if sub-folder structure within category folders is created correctly
        source_folder = os.path.join(self.test_dir, "source_folder")
        target_folder = os.path.join(self.test_dir, "target_folder")
        os.makedirs(source_folder, exist_ok=True)
        os.makedirs(target_folder, exist_ok=True)

        # Create sample files with different extensions
        pdf_file = os.path.join(source_folder, "document.pdf")
        jpg_file = os.path.join(source_folder, "image.jpg")
        zip_file = os.path.join(source_folder, "archive.zip")

        with open(pdf_file, "w") as f:
            f.write("This is a PDF document.")
        with open(jpg_file, "w") as f:
            f.write("This is a JPG image.")
        with open(zip_file, "w") as f:
            f.write("This is a ZIP archive.")

        categories = {
            "pdf_files": (".pdf",),
            "image_files": (".jpg",),
            "zip_files": (".zip",),
        }
        duplicate_action = "skip"

        result = organize_files(source_folder, target_folder, categories, duplicate_action)

        # Ensure that sub-folders within category folders are created
        pdf_subfolder = os.path.join(target_folder, "pdf_files")
        image_subfolder = os.path.join(target_folder, "image_files")
        zip_subfolder = os.path.join(target_folder, "zip_files")

        self.assertTrue(os.path.exists(pdf_subfolder))
        self.assertTrue(os.path.exists(image_subfolder))
        self.assertTrue(os.path.exists(zip_subfolder))

        # Ensure that files are placed in the appropriate sub-folders
        pdf_target_path = os.path.join(pdf_subfolder, "document.pdf")
        jpg_target_path = os.path.join(image_subfolder, "image.jpg")
        zip_target_path = os.path.join(zip_subfolder, "archive.zip")

        self.assertTrue(os.path.exists(pdf_target_path))
        self.assertTrue(os.path.exists(jpg_target_path))
        self.assertTrue(os.path.exists(zip_target_path))

        # Ensure that the result is True (successful)
        self.assertTrue(result)

if __name__ == "__main__":
    unittest.main()
