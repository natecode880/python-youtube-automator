
# YouTube Shorts Upload Scheduler

This project automates the growth of a YouTube channel through the regular upload of short-form content using YouTube Shorts. By following the steps outlined below, you can set up a system to download, rename, shuffle, and schedule TikTok videos for upload to YouTube, ensuring that your channel remains active and engaging with minimal manual intervention.

## Features

- **Automated Video Downloads:** Use the Mass TikTok Video Downloader to download unwatermarked videos.
- **Video Renaming:** Automatically rename video files to remove unnecessary text and prepare them for upload.
- **Video Shuffling:** Randomly shuffle videos from different sources to create a diverse content schedule.
- **Bulk Upload Preparation:** Prepare and organize videos with fixed and filtered hashtags.
- **Automated Scheduling:** Schedule bulk uploads to YouTube at intervals of your choosing.

## Getting Started

### Prerequisites

- Python 3.x installed on your system.
- A Google account with access to the YouTube channel you want to manage.
- Mass TikTok Video Downloader (or any other tool to download unwatermarked TikTok videos).

### Clone the Repository

First, clone this repository to your local machine:

\`\`\`bash
git clone https://github.com/yourusername/YT-Shorts-Upload-Scheduler.git
cd YT-Shorts-Upload-Scheduler
\`\`\`

### Setting Up Your Workspace

1. **Download TikTok Videos:** Use the Mass TikTok Video Downloader to download videos without watermarks.
   - Place videos from one TikTok profile in the \`profile_vids_1\` folder.
   - If you have videos from another profile, place them in the \`profile_vids_2\` folder (or any other folder you wish to name).

2. **Set Up Google Cloud Credentials:**
   - Go to the [Google Cloud Console](https://console.cloud.google.com/).
   - Create a new project and enable the **YouTube Data API v3**.
   - Navigate to **API & Services > Credentials** and create new credentials.
   - Select **OAuth 2.0 Client ID** and set the application type to **Desktop App**.
   - Copy the provided \`client_secret\` and \`client_id\` into the \`credentials.json\` file in the root of your cloned repository.

### Renaming Video Files

To clean up the names of your video files:

1. Open the \`rename_files.py\` script and specify the directory containing your video files.
2. In your terminal, run:

   \`\`\`bash
   python3 rename_files.py
   \`\`\`

   - This will remove unnecessary text from the video filenames.
   - Re-run the script until the filenames contain only the title and hashtags.

### Shuffling Videos

After renaming, shuffle the videos to prepare them for upload:

1. Open the \`shuffle_videos.py\` script.
2. In your terminal, run:

   \`\`\`bash
   python3 shuffle_videos.py
   \`\`\`

   - The script will combine and shuffle videos from different folders into a new folder.

### Preparing Videos for Upload

1. Open the \`prepare_uploads.py\` script.
2. Add as many fixed hashtags as needed. The script will also remove TikTok-specific hashtags like \`#fyp\`.
3. In your terminal, run:

   \`\`\`bash
   python3 prepare_uploads.py
   \`\`\`

   - The processed videos will be copied to the \`ready_uploads\` folder.

### Bulk Uploading and Scheduling

Now that your videos are ready:

1. Open the \`schedule_videos.py\` script.
2. In your terminal, run:

   \`\`\`bash
   python3 schedule_videos.py
   \`\`\`

   - Set your preferred upload interval (e.g., 4 hours or 240 minutes).
   - You'll be redirected to sign in with your Google account linked to your YouTube channel.
   - Grant the required permissions to allow the script to manage your YouTube uploads.
   - Once permissions are granted, the script will automatically schedule all videos in the \`ready_uploads\` folder for upload according to your set interval.

3. Verify your scheduled uploads by checking your YouTube Studio.

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request with your improvements or new features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
