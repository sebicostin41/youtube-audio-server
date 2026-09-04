
from fastapi import FastAPI, HTTPException
import yt_dlp

app = FastAPI()


@app.get("/")
def root():
    return {
        "status": "online",
        "service": "YouTube Audio Server"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.get("/extract")
def extract(video_id: str):
    if not video_id:
        raise HTTPException(
            status_code=400,
            detail="Lipsește video_id"
        )

    youtube_url = f"https://www.youtube.com/watch?v={video_id}"

    options = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "format": "bestaudio[ext=m4a]/bestaudio",
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            info = ydl.extract_info(
                youtube_url,
                download=False
            )

        return {
            "url": info["url"],
            "title": info.get("title", ""),
            "mimeType": info.get(
                "mime_type",
                "audio/mp4"
            )
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
