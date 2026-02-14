"""
Local JSON persistence for EquiVision.
Saves/loads session data to a JSON file so data survives browser refreshes.
No network calls — everything is local and instant.
"""
import json
import os
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")

def _ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def _get_session_file(user_id):
    return os.path.join(DATA_DIR, f"session_{user_id}.json")

# ---------- USERS ----------

def load_users():
    """Load users dict from JSON file."""
    _ensure_dir()
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except:
            pass
    return {}

def save_users(users):
    """Save users dict to JSON file."""
    _ensure_dir()
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def authenticate(username, password):
    """Check credentials. Returns user dict or None."""
    users = load_users()
    user = users.get(username)
    if user and user.get('password') == password:
        return user
    return None

def create_user(username, password):
    """Register a new user. Returns user dict or None if taken."""
    users = load_users()
    if username in users:
        return None  # Already taken
    user = {
        'id': username,  # Use username as ID for simplicity
        'username': username,
        'password': password
    }
    users[username] = user
    save_users(users)
    return user

# ---------- SESSION DATA ----------

def save_session(user_id, events, folders):
    """Save events and folders to a local JSON file."""
    _ensure_dir()
    filepath = _get_session_file(user_id)
    
    # Strip encodings from data to keep file size small
    # Encodings are large float arrays, not needed for persistence
    clean_events = {}
    for eid, evt in events.items():
        clean_evt = dict(evt)
        clean_data = []
        for record in evt.get('data', []):
            r = dict(record)
            r.pop('encoding', None)  # Remove large encoding arrays
            clean_data.append(r)
        clean_evt['data'] = clean_data
        clean_events[eid] = clean_evt
    
    payload = {
        'events': clean_events,
        'folders': folders,
        'saved_at': str(datetime.now())
    }
    
    with open(filepath, 'w') as f:
        json.dump(payload, f, indent=2, default=str)

def load_session(user_id):
    """Load events and folders from local JSON file. Returns (events, folders)."""
    filepath = _get_session_file(user_id)
    if os.path.exists(filepath):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            return data.get('events', {}), data.get('folders', {})
        except:
            pass
    return {}, {}
