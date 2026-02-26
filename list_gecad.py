import requests

URL = "http://192.168.2.91:3456/api/v1"
TOKEN = "tk_a3f9c49bdc19b5fc164ce95e4df6f6df8374f568"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

page = 1
while True:
    r = requests.get(f"{URL}/projects/3/tasks?page={page}", headers=HEADERS)
    tasks = r.json()
    if not tasks: break
    for t in tasks:
        desc = t.get("description", "")
        # Just check a generic task that might have been synced
        if "Source:" in desc or ".md" in desc:
            print(f"Found suspect task: {t['id']} | title={t['title']} | desc={desc}")
    if len(tasks) < 50 or page > 20: break
    page += 1
