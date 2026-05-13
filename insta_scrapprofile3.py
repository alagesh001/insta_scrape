import requests
import re

session = requests.Session()

# =========================================
# HEADERS
# =========================================

headers = {
    "User-Agent": "Mozilla/5.0",
    "x-ig-app-id": "1217981644879628",
    "X-Requested-With": "XMLHttpRequest",
    "Referer": "https://www.instagram.com/",
}

# =========================================
# COOKIES
# =========================================

cookies = {
    "sessionid": "14917812263%3ABQOWWyPv98wcSw%3A26%3AAYiSnz36ch-vUZydyjQ4SwCUCLZujxp8RIdn4_eOPQ",
    "csrftoken": "jAYEU4SZnVvocZuUiJoktwo9IOHaiFut",
}

session.cookies.update(cookies)

# =========================================
# HASHTAG ROUTE REQUEST
# =========================================

url = "https://www.instagram.com/ajax/bulk-route-definitions/"

payload = {
    "route_urls[0]": "/p/DXIBf4gspge/?q=#fitness",
    "__a": "1",
}

response = session.post(
    url,
    headers=headers,
    data=payload
)

text = response.text

print(text[:1000])

# =========================================
# EXTRACT OWNER IDS
# =========================================

owner_ids = re.findall(
    r'"owner_id":"(\d+)"',
    text
)

print("\nOWNER IDS:")
print(owner_ids)