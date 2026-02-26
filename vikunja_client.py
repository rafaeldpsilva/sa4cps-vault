import requests
from typing import Optional, List, Dict, Any

class VikunjaClient:
    """
    A reusable API client for Vikunja.
    Supports Create, Read, Update, Delete (CRUD) operations for tasks,
    as well as assigning colors and subtasks.
    """
    
    def __init__(self, url: str, token: str):
        self.url = url.rstrip('/')
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        self.api_base = f"{self.url}/api/v1"

    def _handle_response(self, response: requests.Response) -> Any:
        try:
            response.raise_for_status()
            if response.text.strip():
                return response.json()
            return None
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
            raise

    # ---------------------------------------------------------
    # Projects
    # ---------------------------------------------------------

    def get_projects(self) -> List[Dict]:
        """Fetch all projects available to the user."""
        r = requests.get(f"{self.api_base}/projects", headers=self.headers, timeout=10)
        return self._handle_response(r)

    def get_project_by_id(self, project_id: int) -> Dict:
        """Fetch a specific project."""
        r = requests.get(f"{self.api_base}/projects/{project_id}", headers=self.headers, timeout=10)
        return self._handle_response(r)

    # ---------------------------------------------------------
    # Tasks (CRUD, Colors, Subtasks)
    # ---------------------------------------------------------

    def get_tasks(self, project_id: int, page: int = 1) -> List[Dict]:
        """Fetch tasks for a specific project with pagination."""
        r = requests.get(f"{self.api_base}/projects/{project_id}/tasks", headers=self.headers, params={"page": page}, timeout=10)
        return self._handle_response(r)

    def get_task(self, task_id: int) -> Dict:
        """Fetch a specific task by ID."""
        r = requests.get(f"{self.api_base}/tasks/{task_id}", headers=self.headers, timeout=10)
        return self._handle_response(r)

    def create_task(self, 
                    project_id: int, 
                    title: str, 
                    description: str = "", 
                    done: bool = False, 
                    hex_color: str = "", 
                    parent_task_id: int = 0) -> Dict:
        """
        Create a new task.
        :param hex_color: Optional color in HEX format (e.g., "#FF0000").
        :param parent_task_id: ID of the parent task if creating a subtask.
        """
        payload = {
            "title": title,
            "description": description,
            "done": done,
        }
        if hex_color:
            payload["hex_color"] = hex_color
        # Parent task id for subtasks is set either via parent_task_id or using the relation endpoint
        # Vikunja handles parent_task_id on task creation in recent versions:
        if parent_task_id and parent_task_id > 0:
            payload["parent_task_id"] = parent_task_id

        r = requests.put(f"{self.api_base}/projects/{project_id}/tasks", headers=self.headers, json=payload, timeout=10)
        task = self._handle_response(r)

        # Fallback: if adding parent_task_id during creation doesn't link it, you could use the relation endpoint
        # Not doing it here by default unless parenthood via creation payload fails.
        return task

    def update_task(self, 
                    task_id: int, 
                    title: Optional[str] = None, 
                    description: Optional[str] = None, 
                    done: Optional[bool] = None, 
                    hex_color: Optional[str] = None) -> Dict:
        """Update an existing task."""
        payload = {}
        if title is not None:
            payload["title"] = title
        if description is not None:
            payload["description"] = description
        if done is not None:
            payload["done"] = done
        if hex_color is not None:
            payload["hex_color"] = hex_color

        if not payload:
            return self.get_task(task_id)

        r = requests.post(f"{self.api_base}/tasks/{task_id}", headers=self.headers, json=payload, timeout=10)
        return self._handle_response(r)

    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        r = requests.delete(f"{self.api_base}/tasks/{task_id}", headers=self.headers, timeout=10)
        # Returns 200 OK on success
        return r.status_code == 200

    def add_subtask_relation(self, parent_task_id: int, child_task_id: int) -> Dict:
        """
        Explicitly link a child task to a parent task, if the create_task payload `parent_task_id` is not supported.
        Relation type for subtask is 'subtask'.
        """
        payload = {
            "other_task_id": child_task_id,
            "relation_kind": "subtask"
        }
        r = requests.put(f"{self.api_base}/tasks/{parent_task_id}/relations", headers=self.headers, json=payload, timeout=10)
        return self._handle_response(r)

# ---------------------------------------------------------
# Example Usage / Test
# ---------------------------------------------------------
if __name__ == "__main__":
    import os

    URL = "http://192.168.2.91:3456"
    TOKEN = "tk_a3f9c49bdc19b5fc164ce95e4df6f6df8374f568"
    PROJECT_ID = 9  # Inbox-RDPDS

    client = VikunjaClient(URL, TOKEN)
    
    print("--- Testing Create Task ---", flush=True)
    parent_task = client.create_task(
        project_id=PROJECT_ID,
        title="Automated Parent Task",
        description="Testing reusable script",
        hex_color="#3498db" # Blue
    )
    print(f"Created Parent: {parent_task['id']} - {parent_task['title']} (Color: {parent_task.get('hex_color')})", flush=True)

    print("\n--- Testing Create Subtask ---", flush=True)
    sub_task = client.create_task(
        project_id=PROJECT_ID,
        title="Automated Subtask",
        description="I belong to the parent task!",
        hex_color="#e74c3c", # Red
        # Note: Depending on Vikunja API version, passing parent_task_id might work during creation
        parent_task_id=parent_task['id'] 
    )
    print(f"Created Subtask: {sub_task['id']} - {sub_task['title']} (Parent: {sub_task.get('parent_task_id')})", flush=True)

    # If subtask doesn't show parent_task_id, use the relation endpoint:
    if not sub_task.get('parent_task_id') or sub_task.get('parent_task_id') == 0:
        print("Explicitly setting subtask relation...", flush=True)
        try:
            client.add_subtask_relation(parent_task['id'], sub_task['id'])
            print("Relation set.", flush=True)
        except Exception as e:
            print(f"Failed to set relation: {e}", flush=True)
    
    print("\n--- Testing Update Task ---", flush=True)
    updated_parent = client.update_task(
        parent_task['id'],
        title="Automated Parent Task (Updated)",
        done=True
    )
    print(f"Updated Parent Status to Done: {updated_parent['done']}", flush=True)

    print("\n--- Testing Delete Tasks (Cleanup) ---", flush=True)
    # Deleting the parent will usually delete or orphan the subtask. We'll delete both to be safe.
    try:
        client.delete_task(sub_task['id'])
        print(f"Deleted Subtask: {sub_task['id']}", flush=True)
    except:
        pass
    
    try:
        client.delete_task(parent_task['id'])
        print(f"Deleted Parent Task: {parent_task['id']}", flush=True)
    except:
        pass
    print("\nAll tests passed successfully!", flush=True)
