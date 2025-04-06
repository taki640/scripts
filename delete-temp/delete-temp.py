import os
import tempfile
import shutil

tempDir = tempfile.gettempdir()
for filename in os.listdir(tempDir):
    filepath = os.path.join(tempDir, filename)
    try:
        if os.path.isfile(filepath) or os.path.islink(filepath):
            os.remove(filepath)
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath)
    except Exception as e:
        print(f"Failed to delete {filepath}: {e}")
