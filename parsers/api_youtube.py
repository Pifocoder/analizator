from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
API_KEY = "AIzaSyCpwuW1KCHsg5Mlv-bdR2KEYpDDdoOxlOM"
# плохо, что виден, но это с ненужной почты :)
# Нужно будет настроить .env
youtube = build("youtube", "v3", developerKey=API_KEY)
SCOPES = 'https://mail.google.com/'
