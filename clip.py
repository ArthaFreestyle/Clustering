import yt_dlp

# --- Helper Function: Ubah "01:30:05" jadi detik ---
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
        'format': 'best[ext=mp4]/best', 
        'outtmpl': output_name,
        'force_keyframes_at_cuts': True, 
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# --- Cara Pakai (Lebih Manusiawi) ---
video_url = "https://www.youtube.com/watch?v=obi7PbNEyeo"

# Sekarang bisa pakai string string kayak gini:
# Format bisa "MM:SS" atau "HH:MM:SS"
create_clip(video_url, "00:57:54", "00:58:19", "clip_keren.mp4") 

print("Selesai!")