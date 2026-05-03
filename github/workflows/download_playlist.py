#!/usr/bin/env python3
import subprocess
import json
import os
import sys
from pathlib import Path

def download_playlist(playlist_url, quality="best"):
    """
    دانلود پلی‌لیست با استفاده از yt-dlp
    """
    
    # تنظیمات دانلود
    output_template = "videos/%(playlist_index)02d - %(title)s.%(ext)s"
    metadata_template = "metadata/%(playlist_index)02d.json"
    
    # دستور yt-dlp
    cmd = [
        "yt-dlp",
        playlist_url,
        "--output", output_template,
        "--write-info-json",  # ذخیره متادیتا
        "--write-thumbnail",   # ذخیره تامنیل
        "--write-description", # ذخیره توضیحات
        "--format", quality,
        "--merge-output-format", "mp4",
        "--restrict-filenames",  # نام فایل استاندارد
        "--no-overwrites",       # بازنویسی نکن
        "--continue",            # ادامه دانلود ناقص
        "--ignore-errors",       # نادیده گرفتن خطاها
        "--no-abort-on-error",   # ادامه با وجود خطا
        "--extract-audio",       # فقط صدا (اختیاری)
        "--audio-format", "mp3", # فرمت صدا
        "--embed-thumbnail",     # تامنیل در فایل
        "--add-metadata"         # اضافه کردن متادیتا
    ]
    
    print(f"شروع دانلود پلی‌لیست: {playlist_url}")
    print(f"کیفیت: {quality}")
    
    try:
        # اجرای دانلود
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("دانلود با موفقیت انجام شد!")
            
            # شمارش فایل‌های دانلود شده
            videos_dir = Path("videos")
            if videos_dir.exists():
                videos = list(videos_dir.glob("*.mp4"))
                print(f"تعداد ویدیوهای دانلود شده: {len(videos)}")
                
                for video in videos:
                    size_mb = video.stat().st_size / (1024 * 1024)
                    print(f"  - {video.name} ({size_mb:.2f} MB)")
        else:
            print(f"خطا در دانلود: {result.stderr}")
            sys.exit(1)
            
    except Exception as e:
        print(f"خطا: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("استفاده: python download_playlist.py <پلی‌لیست_url> [کیفیت]")
        sys.exit(1)
    
    playlist_url = sys.argv[1]
    quality = sys.argv[2] if len(sys.argv) > 2 else "best"
    
    download_playlist(playlist_url, quality)
