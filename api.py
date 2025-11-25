from youtube_transcript_api import YouTubeTranscriptApi
from toon import encode

video_id = 'obi7PbNEyeo' 

ytt_api = YouTubeTranscriptApi()
srt = ytt_api.fetch(video_id=video_id,languages=['id', 'en'])

print(encode(srt.to_raw_data()))