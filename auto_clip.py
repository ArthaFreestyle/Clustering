from google import genai
from google.genai import types
from youtube_transcript_api import YouTubeTranscriptApi
from toon import encode
import yt_dlp
from urllib.parse import urlparse, parse_qs
import json

video_url = "https://www.youtube.com/watch?v=QmqngzMIlV8&t=3s"

# 1. Parse URL
parsed_url = urlparse(video_url)

# 2. Ambil parameter query ('v')
video_id = parse_qs(parsed_url.query)['v'][0]

def time_to_seconds(time_str):
    """Mengubah string HH:MM:SS atau MM:SS menjadi total detik (float)"""
    parts = list(map(float, time_str.split(':')))
    
    # Jika formatnya H:M:S (3 bagian)
    if len(parts) == 3:
        return parts[0] * 3600 + parts[1] * 60 + parts[2]
    # Jika formatnya M:S (2 bagian)
    elif len(parts) == 2:
        return parts[0] * 60 + parts[1]
    # Jika cuma detik
    else:
        return parts[0]

# --- Fungsi Utama ---
def create_clip(url, start_str, end_str, output_name):
    # Konversi dulu string waktu ke detik
    start_sec = time_to_seconds(start_str)
    end_sec = time_to_seconds(end_str)
    
    print(f"Mendownload dari detik ke-{start_sec} sampai {end_sec}...")

    ydl_opts = {
        'download_ranges': lambda info, builder: [
            {'start_time': start_sec, 'end_time': end_sec}
        ],
        'format': 'bestvideo[vcodec^=avc]+bestaudio[ext=m4a]/best[ext=mp4]/best', 
        'outtmpl': output_name,
        'force_keyframes_at_cuts': True, 
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

client = genai.Client(api_key="AIzaSyBdrO5wigwjQxs2wAzS3xhrRXpeWsp0l8s")

ytt_api = YouTubeTranscriptApi()
srt = ytt_api.fetch(video_id=video_id,languages=['id', 'en'])
transkrip_input = encode(srt.to_raw_data())

prompt = f"""
Role:
"Kamu adalah Senior Video Editor dan ahli strategi konten viral untuk TikTok, Instagram Reels, dan YouTube Shorts. Tugasmu adalah membaca transkrip podcast/video berikut dan menemukan segmen-segmen terbaik yang berpotensi viral."

Criteria:
"Sebuah klip dianggap viral jika memenuhi salah satu kriteria ini:
Strong Hook: 3 detik pertama sangat menarik perhatian (kontroversial, mengejutkan, atau relate).
Stand-alone: Klip harus bisa dipahami tanpa menonton video full-nya (konteks lengkap).
Value: Memberikan edukasi, motivasi, atau sangat lucu.
Durasi: Antara 30 detik sampai 60 detik."

Instruction:
"Analisis transkrip yang saya berikan. Pilih 3 klip terbaik.
PENTING: Output harus HANYA berupa format JSON valid tanpa teks pengantar lain. Format JSON sebagai berikut:
JSON
[
{{
"title": "Judul Clickbait yang Menarik (Max 5 kata)",
"start_time": "00:00:00",
"end_time": "00:00:00",
"virality_score": 95,
"reason": "Alasan kenapa klip ini bagus (misal: relatable hook)",
"category": "Motivation/Comedy/News"
}}
]
Gunakan format waktu HH:MM:SS. Pastikan kalimat di awal dan akhir tidak terpotong (tambahkan buffer waktu jika perlu)."

Input Transkrip:
{transkrip_input}
"""

response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=prompt,
    config=types.GenerateContentConfig( # Ganti 'generation_config' jadi 'config'
        response_mime_type="application/json"
    )
)

print(response.text)

clips = json.loads(response.text)

for i,clip in enumerate(clips):
    create_clip(video_url, clip["start_time"], clip["end_time"], f"{i}clip_keren.mp4") 

print("Selesai!")