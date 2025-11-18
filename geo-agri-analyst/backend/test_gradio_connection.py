"""Test Gradio Client connection to HuggingFace Space"""
from gradio_client import Client
import sys

space_name = "HegdeSudarshan/BigEarthNetModels"

print(f"Attempting to connect to: {space_name}")
print("-" * 60)

try:
    client = Client(space_name)
    print(f"✅ Successfully connected!")
    print(f"Client info: {client}")
    print(f"\nAvailable endpoints:")
    print(client.view_api())
except Exception as e:
    print(f"❌ Connection failed!")
    print(f"Error type: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    print("\nFull traceback:")
    import traceback
    traceback.print_exc()
    sys.exit(1)
