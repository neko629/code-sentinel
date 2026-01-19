import unittest
import subprocess
import os

class TestCheckPy(unittest.TestCase):
    def test_default_output(self):
        # Get the directory of check.py relative to the current test file
        check_py_path = os.path.join(os.path.dirname(__file__), "..", "check.py")
        
        # Run check.py as a subprocess and capture its output
        result = subprocess.run(
            ["python", check_py_path],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Assert that the output is "Hello, world!\n"
        self.assertEqual(result.stdout, "Hello, world!\n")
        self.assertEqual(result.stderr, "")

    def test_named_output(self):
        # Get the directory of check.py relative to the current test file
        check_py_path = os.path.join(os.path.dirname(__file__), "..", "check.py")
        
        # Run check.py as a subprocess with an argument and capture its output
        result = subprocess.run(
            ["python", check_py_path, "Gemini"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Assert that the output is "Hello, Gemini!\n"
        self.assertEqual(result.stdout, "Hello, Gemini!\n")
        self.assertEqual(result.stderr, "")

if __name__ == "__main__":
    unittest.main()

