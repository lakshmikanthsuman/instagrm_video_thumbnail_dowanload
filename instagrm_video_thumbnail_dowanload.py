import pandas as pd
import csv
import os
import requests
import re
from transformers import pipeline
from instaloader import Instaloader, Post

# Initialize Hugging Face summarizer
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Initialize Instaloader for Instagram scraping
L = Instaloader()

# Functions

def rewrite_caption(caption):
    """Shorten the Instagram caption using Hugging Face summarization model."""
    print(f"Summarizing caption: {caption}")
    summary = summarizer(caption, max_length=100, min_length=30, do_sample=False)
    print(f"Shortened caption: {summary[0]['summary_text']}")
    return summary[0]['summary_text']

def extract_hashtags(caption):
    """Extract top 3 hashtags from the caption."""
    hashtags = re.findall(r"#\w+", caption)
    return " ".join(hashtags[:3]) if hashtags else ""

def sanitize_filename(name):
    """Convert text to lowercase and replace spaces with underscores"""
    return "_".join(name.lower().split()[:3])

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

def fetch_post_details(post_url, save_video_folder, save_thumbnail_folder):
    """Fetch Instagram post details and download media."""
    print(f"Fetching details for URL: {post_url}")
    shortcode = post_url.split('/')[-2]
    try:
        post = Post.from_shortcode(L.context, shortcode)
        caption = post.caption or ""
        print(f"Original caption: {caption}")
        short_caption = rewrite_caption(caption)
        hashtags = extract_hashtags(caption)
        print(f"Extracted hashtags: {hashtags}")

        # Create sanitized filename
        filename = sanitize_filename(caption) or f"post_{shortcode}"

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

        return caption, short_caption, hashtags
    except Exception as e:
        print(f"❌ Error fetching {post_url}: {e}")
        return None, None, None

# Load CSV with Instagram post links
input_file = r"C:\Users\HP\Downloads\new finone\post link csv\feb_16_27.csv"
df = pd.read_csv(input_file)

# Add new columns for actual captions, shortened captions, and hashtags
df['Actual Caption'] = ""
df['Shortened Caption'] = ""
df['Top 3 Hashtags'] = ""

# Directories to save media files
save_video_folder = r"C:\Users\HP\Downloads\new finone\files dowanloaded\feb 16-27\IG\videos\test"
save_thumbnail_folder = r"C:\Users\HP\Downloads\new finone\files dowanloaded\feb 16-27\IG\thumbnails\test"
output_folder = r"C:\Users\HP\Downloads\new finone\files dowanloaded\feb 16-27\IG"

# Extract filename from input CSV and create output filename
csv_filename = os.path.splitext(os.path.basename(input_file))[0]
output_file = os.path.join(output_folder, f"{csv_filename}_output.xlsx")

# Process each post
for i, row in df.iterrows():
    post_url = row['Post Link']
    if pd.notna(post_url):
        actual_caption, short_caption, hashtags = fetch_post_details(post_url, save_video_folder, save_thumbnail_folder)
        if short_caption:
            df.at[i, 'Actual Caption'] = actual_caption
            df.at[i, 'Shortened Caption'] = short_caption
            df.at[i, 'Top 3 Hashtags'] = hashtags

# Save results to a new Excel file
df.to_excel(output_file, index=False)

print(f"✅ Process completed. Media files saved, and output in '{output_file}'")
