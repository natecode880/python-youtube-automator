import os
import random
import shutil

def gather_videos_from_folders(folder_paths):
    """
    Collects all video files from the specified folder paths.

    This function walks through each folder and its subdirectories to find files
    with video extensions (.mp4, .mov, .avi, .mkv). It organizes the videos
    by folder and returns a list of lists, where each sublist contains the video
    file paths from one folder.

    Args:
        folder_paths (list): A list of folder paths to search for video files.

    Returns:
        list: A list of lists, where each inner list contains video file paths from one folder.
    """
    all_videos = []
    
    # Iterate over each provided folder path.
    for folder in folder_paths:
        folder_videos = []
        
        # Walk through the directory to find video files.
        for root, _, files in os.walk(folder):
            for file in files:
                if file.endswith(('.mp4', '.mov', '.avi', '.mkv')):  # Add other video formats if needed
                    folder_videos.append(os.path.join(root, file))
        
        all_videos.append(folder_videos)
    
    return all_videos

def shuffle_videos(videos):
    """
    Shuffles videos from different folders while ensuring that no more than two consecutive 
    videos come from the same folder.

    The function pops videos from each folder in a round-robin manner and places them 
    into a shuffled list. It then checks for consecutive videos from the same folder 
    and reorders them if necessary.

    Args:
        videos (list): A list of lists, where each inner list contains video file paths from one folder.

    Returns:
        list: A shuffled list of video file paths.
    """
    shuffled_videos = []
    
    # Shuffle videos by popping from each folder's list.
    while any(videos):
        for folder_videos in videos:
            if folder_videos:
                shuffled_videos.append(folder_videos.pop())
    
    # Ensure no more than two consecutive videos from the same folder.
    for i in range(len(shuffled_videos) - 2):
        if (os.path.dirname(shuffled_videos[i]) == os.path.dirname(shuffled_videos[i+1]) == os.path.dirname(shuffled_videos[i+2])):
            for j in range(i+3, len(shuffled_videos)):
                if os.path.dirname(shuffled_videos[j]) != os.path.dirname(shuffled_videos[i]):
                    shuffled_videos[i+2], shuffled_videos[j] = shuffled_videos[j], shuffled_videos[i+2]
                    break
    
    return shuffled_videos

def copy_videos(videos, destination_folder):
    """
    Copies a list of videos to the specified destination folder with renamed filenames.

    The videos are copied to the destination folder with sequentially numbered filenames.
    If the destination folder does not exist, it will be created.

    Args:
        videos (list): A list of video file paths to be copied.
        destination_folder (str): The path to the destination folder where videos will be copied.
    """
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    # Copy each video to the destination folder with a new name.
    for i, video_path in enumerate(videos):
        video_name = os.path.basename(video_path)
        destination_path = os.path.join(destination_folder, f'{i+1:04d}_{video_name}')
        shutil.copy2(video_path, destination_path)
        print(f"Copied {video_path} to {destination_path}")

def main():
    """
    Main function to orchestrate the video shuffling and copying process.

    It gathers videos from the specified folders, shuffles them ensuring no more than two
    consecutive videos from the same folder, and then copies them to the destination folder.
    """
    # List of folders containing different videos of different profiles (add actual paths)
    folder_paths = [
        'profile_vids_1',
        'profile_vids_2', # Add more if necessary
    ]
    
    # Destination folder to copy shuffled videos
    destination_folder = 'shuffled_uploads'

    # Gather all videos from specified folders
    videos_by_folder = gather_videos_from_folders(folder_paths)
    videos = [video for folder in videos_by_folder for video in folder]
    print(f"Found {len(videos)} videos.")

    # Shuffle videos ensuring no more than two consecutive videos from the same folder
    shuffled_videos = shuffle_videos(videos_by_folder)

    # Copy shuffled videos to the destination folder
    copy_videos(shuffled_videos, destination_folder)

if __name__ == '__main__':
    main()
