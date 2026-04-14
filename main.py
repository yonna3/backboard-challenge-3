import asyncio
import os
import dotenv
from backboard import BackboardClient

# Load variables from the .env file
dotenv.load_dotenv()

async def main():
    # Fixed: Changed get_env to getenv
    api_key = os.getenv("BACKBOARD_API_KEY")
    
    if not api_key:
        print("❌ Error: BACKBOARD_API_KEY not found in .env file!")
        return

    client = BackboardClient(api_key=api_key)

    try:
        # --- Step 1: Create an Assistant ---
        assistant = await client.create_assistant(
            name="My First Assistant",
            system_prompt="You are a helpful assistant that responds concisely."
        )
        print(f"✅ Created assistant: {assistant.assistant_id}")

        # --- Step 2: Create a Thread ---
        thread = await client.create_thread(assistant_id=assistant.assistant_id)
        print(f"✅ Created thread: {thread.thread_id}")

        # --- Step 3: Send a Message (Non-Streaming) ---
        print("Sending message...")
        response = await client.add_message(
            thread_id=thread.thread_id,
            content="say Hello World",
            stream=False
        )
        print(f"🤖 Assistant: {response.content}")

    except Exception as e:
        print(f"❌ An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())