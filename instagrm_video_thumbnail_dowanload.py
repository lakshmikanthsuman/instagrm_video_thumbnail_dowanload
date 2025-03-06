import csv
import os
import requests
import re
from instaloader import Instaloader, Post

def sanitize_filename(name):
    """Convert text to lowercase and replace spaces with underscores"""
    return "_".join(name.lower().split()[:3])

def download_instagram_post(post_url, save_video_folder, save_thumbnail_folder):
    loader = Instaloader()
    shortcode = post_url.rstrip('/').split('/')[-1]  # Extract shortcode from URL
    
    try:
        post = Post.from_shortcode(loader.context, shortcode)
        caption_text = post.caption or "default_name"
        filename = sanitize_filename(caption_text)
        
        # Download video if available
        if post.is_video:
            video_url = post.video_url
            video_path = os.path.join(save_video_folder, f"{filename}.mp4")
            download_file(video_url, video_path)
            print(f"✅ Video downloaded: {video_path}")
        
        # Download thumbnail
        thumbnail_url = post.url
        thumbnail_path = os.path.join(save_thumbnail_folder, f"{filename}.jpg")
        download_file(thumbnail_url, thumbnail_path)
        print(f"✅ Thumbnail downloaded: {thumbnail_path}")
    
    except Exception as e:
        print(f"❌ Error processing {post_url}: {e}")

def download_file(url, filepath):
    """Download a file from a URL and save it locally"""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    else:
        print(f"❌ Failed to download: {url}")

def process_csv(csv_path, save_video_folder, save_thumbnail_folder):
    with open(csv_path, newline='', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader, None)  # Skip header if present
        for row in reader:
            if row:
                download_instagram_post(row[0], save_video_folder, save_thumbnail_folder)

if __name__ == "__main__":
    csv_path = r"C:\Users\HP\Downloads\new finone\post link csv\feb_16_27.csv"
    save_video_folder = r"C:\Users\HP\Downloads\new finone\files dowanloaded\feb 16-27\IG\videos"
    save_thumbnail_folder = r"C:\Users\HP\Downloads\new finone\files dowanloaded\feb 16-27\IG\thumbnails"
    
    process_csv(csv_path, save_video_folder, save_thumbnail_folder)
