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
print(f"Searching hashtag: #{HASHTAG}")

hashtag = instaloader.Hashtag.from_name(L.context, HASHTAG)

users_data = {}
count = 0

for post in hashtag.get_posts():
    try:
        username = post.owner_username

        # Skip duplicates
        if username in users_data:
            continue

        profile = instaloader.Profile.from_username(L.context, username)

        users_data[username] = {
            "Influencer Name": profile.full_name,
            "Instagram URL": f"https://instagram.com/{username}",
            "Followers": profile.followers,
            "Category/Hashtag": HASHTAG,
            "Bio": profile.biography,
        }

        print(f"Collected: {username}")

        count += 1

        # Rate limit protection
        time.sleep(3)

        if count >= POST_LIMIT:
            break

    except Exception as e:
        print(f"Error: {e}")
        continue

# =========================
# SAVE CSV
# =========================
df = pd.DataFrame(users_data.values())
df.to_csv(OUTPUT_FILE, index=False)

print("\nDone!")
print(f"Saved to: {OUTPUT_FILE}")