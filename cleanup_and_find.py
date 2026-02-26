import requests
import sys

URL = "http://192.168.2.91:3456/api/v1"
TOKEN = "tk_a3f9c49bdc19b5fc164ce95e4df6f6df8374f568"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

try:
    print("Fetching projects...", flush=True)
    r = requests.get(f"{URL}/projects", headers=HEADERS, timeout=10)
    projects = r.json()

    target_project_id = None
    wrong_project_id = 3

    print("Projects found:", flush=True)
    for p in projects:
        print(f"ID: {p['id']}, Title: {p['title']}", flush=True)
        if p['title'] == 'inbox-rdpds':
            target_project_id = p['id']

    if target_project_id:
        print(f"\nFound target project 'inbox-rdpds' with ID: {target_project_id}", flush=True)
    else:
        print("\nCould not find 'inbox-rdpds'!", flush=True)

    print(f"\nCleaning up tasks from wrong project {wrong_project_id}...", flush=True)
    page = 1
    deleted = 0
    while True:
        r = requests.get(f"{URL}/projects/{wrong_project_id}/tasks?page={page}", headers=HEADERS, timeout=10)
        if r.status_code != 200:
            break
        try:
            tasks = r.json()
        except:
            break
        if not tasks or not isinstance(tasks, list):
            break
        
        for t in tasks:
            description = t.get("description", "")
            if "Source: " in description:
                del_r = requests.delete(f"{URL}/tasks/{t['id']}", headers=HEADERS, timeout=10)
                if del_r.status_code == 200:
                    deleted += 1
                    print(f"Deleted task '{t['title']}'", flush=True)
                else:
                    print(f"Failed to delete '{t['title']}': {del_r.status_code}", flush=True)
        
        if len(tasks) < 50 or page > 20: # cap pages
            break
        page += 1

    print(f"Cleanup finished. Deleted {deleted} tasks from GECAD.", flush=True)

except Exception as e:
    print("Error:", e, flush=True)
