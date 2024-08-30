import os
import shutil

# Just an extra program if you would like to clear your folder
def clear_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
                print(f"Deleted file: {file_path}")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"Deleted directory: {file_path}")
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

def main():
    folder_path = 'ready_uploads_stonktech'  
    clear_folder(folder_path)
    print("Folder cleared.")

if __name__ == '__main__':
    main()
