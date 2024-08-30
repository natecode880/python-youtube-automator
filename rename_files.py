import os

# Re-run file until the name of the files in the directory contains only title and hashtags like it does on TikTok
# Directory containing the files - Directory of file containing videos
directory = ''  # In the quotation marks add the directory of the profile_vids_n 

# Function to rename files
def rename_files(directory):
    for filename in os.listdir(directory):
        if "_" in filename:
            # Strip everything before and including the first underscore
            new_filename = filename.split('_', 1)[-1]  # Split by '_' and take the part after the first underscore
            new_filepath = os.path.join(directory, new_filename)
            old_filepath = os.path.join(directory, filename)
            
            # Rename the file
            os.rename(old_filepath, new_filepath)
            print(f'Renamed: {filename} -> {new_filename}')

# Call the function
rename_files(directory)
