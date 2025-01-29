import os
import shutil

def delete_pycache(start_path):
    """
    Recursively deletes all __pycache__ folders starting from the given path.
    """
    for root, dirs, files in os.walk(start_path):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            shutil.rmtree(pycache_path)
            print(f"Deleted: {pycache_path}")

if __name__ == "__main__":
    path = "../"
    delete_pycache(path)
