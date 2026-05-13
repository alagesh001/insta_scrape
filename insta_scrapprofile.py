import instaloader
import pandas as pd
import time

# =========================
# CONFIG
# =========================
# =========================
# CONFIG
# =========================
HASHTAG = "fitness"
POST_LIMIT = 10
OUTPUT_FILE = f"{HASHTAG}_influencers.csv"

USERNAME = "zebs.sa"
T_USERNAME = "jjameswebster"

# =========================
# INSTALOADER SETUP
# =========================
L = instaloader.Instaloader(
    download_pictures=False,
    download_videos=False,
    download_comments=False,
    save_metadata=False,
)

# =========================
# LOGIN USING SAVED SESSION
# =========================
try:
    L.load_session_from_file(USERNAME)
    print("Session loaded successfully")

except FileNotFoundError:
    print("No saved session found")
    print("Logging in interactively...")

    L.interactive_login(USERNAME)

    L.save_session_to_file()

    print("Session saved successfully")

# =========================
# GET HASHTAG POSTS
# =========================
profile = instaloader.Profile.from_username(L.context, "actorvijay")

# 4. Extract specific data
print(f"Username: {profile.username}")
print(f"User ID: {profile.userid}")
print(f"Followers: {profile.followers}")
print(f"Following: {profile.followees}")
print(f"Bio: {profile.biography}")
print(f"Total Posts: {profile.mediacount}")