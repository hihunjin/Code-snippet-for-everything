!pip install slack-sdk
import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

def upload_file(file_path, channel_id: str, slack_token: str, initial_comment=None):
    """
    channel_id: "C0........"
    slack_token: "xo..-........"
    """
    client = WebClient(token=slack_token)
    try:
        response = client.files_upload_v2(
            channel=channel_id,
            filename=file_path,
            file=file_path,
            initial_comment=initial_comment,
            title=os.path.basename(file_path)
        )
        print("File uploaded successfully.")
    except SlackApiError as e:
        print(f"Error uploading file: {e}")
