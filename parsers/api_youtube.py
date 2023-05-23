from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
API_KEY = "AIzaSyDoDH0lnFrG1siG3Pwh-ui8VQwmUzh4vP0"
# плохо, что виден, но это с ненужной почты :)
# Нужно будет настроить .env
youtube = build("youtube", "v3", developerKey=API_KEY)
SCOPES = 'https://mail.google.com/'
