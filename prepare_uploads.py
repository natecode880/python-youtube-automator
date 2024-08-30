import os  # Provides functions to interact with the operating system
import random  # Used for random selection and shuffling
import shutil  # Used for high-level file operations like copying

# Predefined set of hashtags to include in video titles
fixed_hashtags = [
    "#mainhashtag1", "#mainhashtags2", "mainhashtag3",  # Add as many hashtags as needed
]

# Hashtags to exclude from video titles
excluded_hashtags = ['#fyp', '#fy', '#tiktok']

def filter_original_hashtags(hashtags):
    """
    Filters out hashtags that are either excluded, start with '#f', or contain '@'.
    
    Args:
    hashtags (list): List of hashtags to filter.

    Returns:
    list: Filtered list of hashtags.
    """
    return [tag for tag in hashtags if not (tag.startswith('#f') or '@' in tag or tag in excluded_hashtags)]

def shuffle_and_process_videos(source_folder, destination_folder, fixed_hashtags):
    """
    Shuffles and processes video files from the source folder, appending hashtags to the video titles,
    and copies them to the destination folder.

    Args:
    source_folder (str): Path to the folder containing the original videos.
    destination_folder (str): Path to the folder where processed videos will be saved.
    fixed_hashtags (list): List of fixed hashtags to append to video titles.

    Returns:
    tuple: Counts of videos with title lengths below or above 100 characters.
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    video_files = []

    # Walk through the source folder to collect video files
    for root, _, files in os.walk(source_folder):
        for file in files:
            if file.endswith(('.mp4', '.mov', '.avi', '.mkv')):  # Supported video formats
                video_files.append(os.path.join(root, file))
    
    # Shuffle the list of video files randomly
    random.shuffle(video_files)

    below_100_count = 0
    above_100_count = 0

    for file_path in video_files:
        file = os.path.basename(file_path)
        base_title, _ = os.path.splitext(file)
        
        # Separate words, emojis, and original hashtags from the title
        title_parts = base_title.split()
        words_and_emojis = [part for part in title_parts if not part.startswith('#')]
        original_hashtags = [part for part in title_parts if part.startswith('#')]
        filtered_original_hashtags = filter_original_hashtags(original_hashtags)

        # Select 3 random hashtags from the fixed set
        random_hashtags = random.sample(fixed_hashtags, 3)

        # Construct the new title with selected hashtags and original ones
        new_title = f"{' '.join(words_and_emojis)} #shorts {' '.join(random_hashtags)} {' '.join(filtered_original_hashtags)}"
        new_file_name = f"{new_title}.mp4"
        new_file_path = os.path.join(destination_folder, new_file_name)

        # Check the length of the new title and update counters
        if len(new_title) <= 100:
            below_100_count += 1
        else:
            above_100_count += 1

        # Copy the video file with the new title to the destination folder
        shutil.copy2(file_path, new_file_path)
        print(f"Copied {file} to {new_file_name}")

    return below_100_count, above_100_count

def main():
    """
    Main function to execute the video processing workflow.
    """
    source_folder = 'shuffled_uploads'  # Path to the folder with shuffled videos
    destination_folder = 'ready_uploads'  # Path to save processed videos

    # Process the videos and retrieve counts of title lengths
    below_100_count, above_100_count = shuffle_and_process_videos(source_folder, destination_folder, fixed_hashtags)
    
    print(f"Total videos with title length <= 100 characters: {below_100_count}")
    print(f"Total videos with title length > 100 characters: {above_100_count}")

if __name__ == '__main__':
    main()
