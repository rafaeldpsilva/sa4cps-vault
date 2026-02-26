import os
import re
import requests
import json
import sys
import requests
import json

VAULT_PATH = "/home/rdpds/Obsidian/phd-vault"
API_URL = "http://192.168.2.91:3456/api/v1"
TOKEN = "tk_a3f9c49bdc19b5fc164ce95e4df6f6df8374f568"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Task regex pattern
TASK_PATTERN = re.compile(r"^[ \t]*-[ \t]+\[([xX ]+)\][ \t]+(.*)")

def get_projects():
    print("Fetching projects from Vikunja...", flush=True)
    r = requests.get(f"{API_URL}/projects", headers=HEADERS, timeout=10)
    if r.status_code == 200:
        return r.json()
    else:
        print(f"Failed to fetch projects. Status: {r.status_code}, Body: {r.text}")
        return []

def get_existing_tasks(project_id):
    print(f"Fetching existing tasks for project {project_id}...", flush=True)
    # Vikunja pagination by default is 50. We might need pagination if large.
    page = 1
    all_tasks = []
    while True:
        r = requests.get(f"{API_URL}/projects/{project_id}/tasks?page={page}", headers=HEADERS, timeout=10)
        if r.status_code != 200:
            break
        try:
            tasks = r.json()
        except:
            break
        if not tasks or not isinstance(tasks, list):
            break
        all_tasks.extend(tasks)
        print(f"Fetched {len(tasks)} tasks from page {page}", flush=True)
        if len(tasks) < 50 or page > 20: # cap at 20 pages or if less than max page size
            break
        page += 1
    return {t["title"]: t for t in all_tasks}

def create_task(project_id, title, is_done, description=""):
    payload = {
        "title": title,
        "done": is_done,
        "description": description
    }
    r = requests.put(f"{API_URL}/projects/{project_id}/tasks", headers=HEADERS, json=payload, timeout=10)
    if r.status_code in [200, 201]:
        print(f"Successfully created task: {title}", flush=True)
    else:
        print(f"Failed to create task: {title} | Error: {r.text}", flush=True)

def update_task_status(task_id, is_done):
    payload = {
        "done": is_done
    }
    r = requests.post(f"{API_URL}/tasks/{task_id}", headers=HEADERS, json=payload, timeout=10)
    if r.status_code == 200:
        print(f"Updated status for task ID {task_id} to done={is_done}")
    else:
        print(f"Failed to update task ID {task_id}")

def find_vault_tasks():
    tasks = []
    for root, dirs, files in os.walk(VAULT_PATH):
        if ".git" in root or ".obsidian" in root:
            continue
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, "r", encoding="utf-8") as f:
                        for line in f:
                            match = TASK_PATTERN.match(line)
                            if match:
                                state_char = match.group(1).strip()
                                is_done = (state_char.lower() == 'x')
                                title = match.group(2).strip()
                                # remove markdown links [like this](...) or [[links]] from title if we wanted, but vikunja supports md
                                if title:
                                    # include filepath as description trace
                                    rel_path = os.path.relpath(filepath, VAULT_PATH)
                                    tasks.append({
                                        "title": title,
                                        "done": is_done,
                                        "file": rel_path
                                    })
                except Exception as e:
                    print(f"Could not read {file}: {e}")
    return tasks

def main():
    projects = get_projects()
    if not projects:
        print("No Vikunja projects found!")
        return

    target_project = projects[0]
    for p in projects:
        if p.get("title") == "inbox-rdpds":
            target_project = p
            break
    
    project_id = target_project["id"]
    print(f"Using project: {target_project.get('title')} (ID: {project_id})", flush=True)

    existing_tasks = get_existing_tasks(project_id)
    print(f"Found {len(existing_tasks)} existing tasks in Vikunja.", flush=True)

    vault_tasks = find_vault_tasks()
    print(f"Found {len(vault_tasks)} tasks in Obsidian vault.", flush=True)

    for vt in vault_tasks:
        vt_title = vt["title"]
        vt_done = vt["done"]
        desc = f"Source: {vt['file']}"
        
        # Avoid exact title duplicates
        if vt_title in existing_tasks:
            ex_task = existing_tasks[vt_title]
            if ex_task.get("done") != vt_done:
                # Sync status if it changed
                update_task_status(ex_task["id"], vt_done)
            else:
                pass # Already synced and up to date
        else:
            # Create new
            create_task(project_id, vt_title, vt_done, desc)
            # Add to dict to catch duplicates within the same vault
            existing_tasks[vt_title] = {"id": -1, "done": vt_done, "title": vt_title}

if __name__ == "__main__":
    main()
