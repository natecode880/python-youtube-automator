import os
import pickle
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pytz

# Define the required OAuth 2.0 scopes for accessing YouTube Data API v3.
# If you modify these scopes, ensure to delete the 'token.pickle' file 
# to force re-authentication with the updated scopes.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']

def get_authenticated_service():
    """
    Authenticate the user and return an authorized YouTube Data API service instance.

    If a valid authentication token exists (stored in 'token.pickle'), it will be loaded.
    If the token is expired or doesn't exist, the user will be prompted to authenticate.
    The new credentials will be saved to 'token.pickle' for future use.
    
    Returns:
        googleapiclient.discovery.Resource: Authorized YouTube Data API service instance.
    """
    creds = None
    
    # Load credentials from 'token.pickle' if the file exists.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials are found, prompt the user to authenticate.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        # Save the new credentials to 'token.pickle'.
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    # Build and return the authorized YouTube service instance.
    return build('youtube', 'v3', credentials=creds)

def list_uploaded_videos(youtube):
    """
    Retrieve a list of uploaded videos from the authenticated user's YouTube channel.

    This function fetches the upload playlist ID from the user's channel and 
    then retrieves all videos in that playlist.

    Args:
        youtube (googleapiclient.discovery.Resource): Authorized YouTube Data API service instance.

    Returns:
        list: A list of video resources in the upload playlist.
    """
    request = youtube.channels().list(
        part='contentDetails',
        mine=True
    )
    response = request.execute()
    
    # Extract the playlist ID for uploaded videos.
    uploads_playlist_id = response['items'][0]['contentDetails']['relatedPlaylists']['uploads']

    videos = []
    nextPageToken = None
    
    # Paginate through the uploaded videos playlist.
    while True:
        request = youtube.playlistItems().list(
            part='snippet',
            maxResults=50,
            playlistId=uploads_playlist_id,
            pageToken=nextPageToken
        )
        response = request.execute()
        
        # Accumulate video resources.
        videos.extend(response['items'])
        nextPageToken = response.get('nextPageToken')
        
        # Exit loop if no more pages are available.
        if not nextPageToken:
            break
    
    return videos

def schedule_videos(youtube, videos):
    """
    Schedule the publication of a list of videos at regular intervals.

    The first video will be scheduled 5 minutes from the current time, 
    and subsequent videos will be scheduled at intervals of 240 minutes 
    (or a different interval if specified).

    Args:
        youtube (googleapiclient.discovery.Resource): Authorized YouTube Data API service instance.
        videos (list): A list of video resources to be scheduled.
    """
    start_time = datetime.datetime.now(pytz.UTC) + datetime.timedelta(minutes=5)
    interval = datetime.timedelta(minutes=240)  # Adjust the interval as necessary
    
    # Schedule each video at the calculated time.
    for video in videos:
        schedule_video(youtube, video['snippet']['resourceId']['videoId'], start_time)
        start_time += interval

def schedule_video(youtube, video_id, publish_time):
    """
    Schedule a single video for publication at a specified time.

    The video is initially set to private and will be made public 
    at the scheduled publish time.

    Args:
        youtube (googleapiclient.discovery.Resource): Authorized YouTube Data API service instance.
        video_id (str): The ID of the video to be scheduled.
        publish_time (datetime): The UTC datetime when the video should be published.
    """
    publish_time_str = publish_time.strftime('%Y-%m-%dT%H:%M:%S.000Z')
    print(f"Scheduling video {video_id} to be published at {publish_time_str}")
    
    request = youtube.videos().update(
        part="status",
        body={
            "id": video_id,
            "status": {
                "privacyStatus": "private",  # Initially set to private
                "publishAt": publish_time_str  # Scheduled publish time
            }
        }
    )
    
    try:
        # Execute the API request to schedule the video.
        response = request.execute()
        print(f"Scheduled video {video_id} to be published at {publish_time_str}")
    except Exception as e:
        error_message = str(e)
        
        # Handle known non-critical errors gracefully.
        if "Some specific error detail" in error_message:
            print(f"Warning: A non-critical issue occurred while scheduling video {video_id}: {error_message}")
        else: 
            print(f"Failed to schedule video {video_id}: {e}")
            raise

if __name__ == '__main__':
    # Authenticate and build the YouTube service.
    youtube = get_authenticated_service()
    
    # Retrieve the list of uploaded videos.
    videos = list_uploaded_videos(youtube)
    
    # Schedule the videos for publication.
    schedule_videos(youtube, videos)
