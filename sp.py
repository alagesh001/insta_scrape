from playwright.sync_api import sync_playwright
import requests
import re
import json
import pandas as pd
import time

HASHTAG = "psychologist"
SCROLL_COUNT = 5

results = []

with sync_playwright() as p:
    iphone = p.devices["iPhone 13"]

    browser = p.chromium.launch(
        headless=False
    )

    context = browser.new_context(
        **iphone
    )

    page = context.new_page()

    # =========================================
    # LOGIN MANUALLY FIRST
    # =========================================

    page.goto("https://www.instagram.com/accounts/login/")
    print("\nLogin manually...")
    page.wait_for_url("https://www.instagram.com/*", timeout=300000)
    print("Login detected!")

    # =========================================
    # COLLECT OWNER IDS
    # =========================================

    owner_ids = set()

    def handle_response(response):

        try:

            url = response.url

            # Detect Instagram route preload requests
            if "bulk-route-definitions/" in url or "bz?" in url:
                print("\nURL:", url)
                body = response.body()
                text = body.decode("utf-8", errors="ignore")
                #print(text[:3000])

                ids = re.findall(
                r'"owner_id"\s*:\s*"(\d+)"',
                text
                )


                for i in ids:
                    owner_ids.add(i)

                print(f"Collected IDs: {len(owner_ids)}")

        except:
            pass

    page.on("response", handle_response)

    # =========================================
    # OPEN HASHTAG SEARCH
    # =========================================

    page.goto(
        f"https://www.instagram.com/explore/search/keyword/?q=%23{HASHTAG}"
    )

    time.sleep(5)

    # =========================================
    # AUTO SCROLL
    # =========================================

    for _ in range(SCROLL_COUNT):

        page.mouse.wheel(0, 8000)

        time.sleep(3)

    print("\nTotal Owner IDs:", len(owner_ids))

    # =========================================
    # GET BROWSER COOKIES
    # =========================================

    cookies = context.cookies()

    cookie_dict = {}

    for c in cookies:
        cookie_dict[c["name"]] = c["value"]

    # =========================================
    # REQUESTS SESSION
    # =========================================

    session = requests.Session()

    session.cookies.update(cookie_dict)

    headers = {
        "User-Agent": "Mozilla/5.0",
        "x-ig-app-id": "1217981644879628",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/",
    }

    # =========================================
    # FETCH PROFILE INFO
    # =========================================

    for user_id in owner_ids:

        try:

            url = (
                f"https://www.instagram.com/api/v1/"
                f"users/{user_id}/info/"
            )

            r = session.get(
                url,
                headers=headers
            )

            if r.status_code != 200:
                print("Failed:", user_id)
                continue

            data = r.json()

            user = data["user"]

            bio = ""

            if "biography_with_entities" in user:
                bio = user["biography_with_entities"]["raw_text"]

            results.append({
                "Influencer Name": user.get("full_name"),
                "Username": user.get("username"),
                "Instagram URL":
                    f"https://instagram.com/{user.get('username')}",
                "Followers": user.get("follower_count"),
                "Category": user.get("category"),
                "Bio": bio,
            })

            print("Collected:",
                  user.get("username"))

            time.sleep(2)

        except Exception as e:
            print("Error:", e)

  #  browser.close()

# =========================================
# SAVE CSV
# =========================================

df = pd.DataFrame(results)

df.to_csv(
    f"{HASHTAG}_influencers.csv",
    index=False
)

print("\nDONE!")
print(df.head())