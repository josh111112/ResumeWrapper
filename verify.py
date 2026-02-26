from utils import extract_text
import io

class MockFile:
    def __init__(self, name, content):
        self.name = name
        self.content = content
    def read(self):
        return self.content

try:
    f = MockFile("test.txt", b"Hello World")
    text = extract_text(f)
    print(f"Extracted Text: {text}")

    if text == "Hello World":
        print("SUCCESS")
    else:
        print("FAILURE")
except Exception as e:
    print(f"ERROR: {e}")
