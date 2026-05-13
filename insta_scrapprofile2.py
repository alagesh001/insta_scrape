import requests
import json

# username = "jjameswebster"

# url = (
#     f"https://www.instagram.com/api/v1/"
#     f"users/web_profile_info/?username={username}"
# )
user_id = "11568805610"

url = (
    f"https://www.instagram.com/api/v1/"
    f"users/{user_id}/info/"
)
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/136.0.0.0 Safari/537.36"
    ),
    "x-ig-app-id": "1217981644879628",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.instagram.com/",
}

# Paste REAL cookies here
cookies = {
    "sessionid": "14917812263%3ABQOWWyPv98wcSw%3A26%3AAYiSnz36ch-vUZydyjQ4SwCUCLZujxp8RIdn4_eOPQ",
    "csrftoken": "jAYEU4SZnVvocZuUiJoktwo9IOHaiFut"
}

response = requests.get(
    url,
    headers=headers,
    cookies=cookies
)

print("Status:", response.status_code)

print(response.text)

if response.status_code == 200:

    data = response.json()

    user = data["user"]
    print("\nusername:", user["username"])

    print("Name:", user["full_name"])
    print("Followers:", user["follower_count"])
    print("Bio:",user["biography"])