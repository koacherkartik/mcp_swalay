from dotenv import load_dotenv
import os
import signal
import sys
import json
import time

from app.ai import LocalAI
from app.executor import CommandExecutor

load_dotenv()


def shutdown_handler(signum, frame):
    print("\nShutdown requested, stopping cleanly...")
    sys.exit(0)


signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)

print("=" * 50)
print("DRDO OFFLINE MCP SERVER")
print("=" * 50)

print("Mongo URI :", os.getenv("MONGO_URI"))
print("Database  :", os.getenv("DATABASE_NAME"))
print("Model     :", os.getenv("MODEL_NAME"))

# Initialize AI and Executor
print("\nInitializing AI model...")
ai = LocalAI()

print("Initializing MongoDB executor...")
executor = CommandExecutor()

print("\nServer Started and Ready for Commands!\n")

while True:
    try:
        # Get command from user
        user_command = input("\n📝 Enter your command in English (or 'exit' to quit):\n> ").strip()
        
        if user_command.lower() == 'exit':
            print("\nGoodbye!")
            break
        
        if not user_command:
            print("⚠️  Please enter a command.")
            continue
        
        print("\n⏳ Processing your command...")
        
        # Translate English to MongoDB JSON using AI
        print("🤖 Translating command using AI...")
        command = ai.generate(user_command)
        print(f"✅ Translated command: {json.dumps(command, indent=2)}")
        
        # Execute the command
        print("\n⚙️  Executing command...")
        result = executor.execute(command)
        
        print(f"\n✨ Result:")
        print(json.dumps(result, indent=2, default=str))
        
    except KeyboardInterrupt:
        print("\n\nShutdown requested...")
        break
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()