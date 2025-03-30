import json
import yt_dlp
from pydub import AudioSegment
import subprocess
import os
import re

# Dependencies: pip install yt-dlp pydub openai-whisper vosk soundfile numpy

async def process_mystery_transcription(youtube_url: str, start_time: float, end_time: float):
    """
    Downloads a YouTube video, extracts audio for the specified segment,
    transcribes it using Whisper, and returns the transcription as plain text.
    """
    try:
        video_output = "mystery_video.mp4"

        ydl_opts = {'format': 'bestaudio/best', 'outtmpl': video_output}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])

        audio_output = "mystery_audio.mp3"
        AudioSegment.from_file(video_output).export(audio_output, format="mp3")

        # Convert seconds to milliseconds
        audio = AudioSegment.from_file(audio_output)
        segment = audio[int(start_time * 1000):int(end_time * 1000)]
        segment.export("mystery_segment.wav", format="wav")

        # Transcribe with Whisper
        transcription = subprocess.run(
            ["whisper", "mystery_segment.wav", "--model", "small"],
            capture_output=True, text=True
        )
        transcript_text = transcription.stdout.strip()

        # ✅ Step 1: Remove unwanted metadata (e.g., "Detecting language...")
        transcript_text = re.sub(r"Detecting language.*?Detected language: \w+\s*", "", transcript_text, flags=re.DOTALL)

        # ✅ Step 2: Remove timestamps (e.g., "[00:00.000 --> 00:03.340]")
        transcript_text = re.sub(r"\[\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}\.\d{3}\] ", "", transcript_text)

        # ✅ Step 3: Remove newlines and extra spaces
        transcript_text = " ".join(transcript_text.split())

        # Cleanup temporary files
        os.remove(video_output)
        os.remove(audio_output)
        os.remove("mystery_segment.wav")

        return {"answer": transcript_text}  # ✅ Clean output

    except Exception as e:
        return {"error": f"Failed to process transcription: {str(e)}"}
