import os
import requests
import dotenv

dotenv.load_dotenv()

# --- CONFIGURATION ---
API_KEY = os.getenv("BACKBOARD_API_KEY")
ASSISTANT_ID = "4e24ca63-63ba-4a62-ad83-e8e367748e5c" 
HEADERS = {"X-API-Key": API_KEY, "Content-Type": "application/json"}
# Note: Added /v1 if required by the latest docs, otherwise kept app.backboard.io
BASE_URL = "https://app.backboard.io/api"

def check_response(response, step_name):
    if response.status_code in [200, 201]: # 201 is "Created"
        print(f"✅ {step_name} Success!")
        return response.json()
    else:
        print(f"❌ {step_name} Failed: {response.status_code} - {response.text}")
        return None

def main():
    # --- Step 1: Create a Thread (Fixed Endpoint) ---
    print("--- Creating Thread ---")
    # Some APIs prefer /threads/ with a slash
    thread_resp = requests.post(
        f"{BASE_URL}/threads", 
        headers=HEADERS, 
        json={"assistant_id": ASSISTANT_ID}
    )
    thread = check_response(thread_resp, "Create Thread")
    
    if not thread:
        # Debugging: Try the alternate endpoint format if the first fails
        print("Retrying with alternate endpoint...")
        thread_resp = requests.post(f"{BASE_URL}/assistants/{ASSISTANT_ID}/threads", headers=HEADERS)
        thread = check_response(thread_resp, "Create Thread (Alt)")
        if not thread: return

    thread_id = thread['thread_id']

    # --- Step 2: Send Message ---
    print("\n--- Sending Message with Memory/Search ---")
    msg_data = {
        "content": "I prefer Python over JavaScript. What's the latest in AI?",
        "web_search": "auto",
        "memory": "Auto"
    }
    msg_resp = requests.post(
        f"{BASE_URL}/threads/{thread_id}/messages", 
        headers=HEADERS, 
        json=msg_data
    )
    check_response(msg_resp, "Send Message")

    # --- Step 7: Check Stats (Easiest way to verify it's working) ---
    print("\n--- Checking Memory Stats ---")
    stats_resp = requests.get(f"{BASE_URL}/assistants/{ASSISTANT_ID}/memories/stats", headers=HEADERS)
    check_response(stats_resp, "Memory Stats")

if __name__ == "__main__":
    main()