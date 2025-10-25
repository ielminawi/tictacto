#!/usr/bin/env python3
"""
Simple launcher for LiveKit Agent
"""

import subprocess
import time
import webbrowser
import os
import sys

def main():
    print("🚀 Starting LiveKit Agent...")
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ main.py not found. Please run this script from the galactactocus directory.")
        input("Press Enter to exit...")
        return
    
    if not os.path.exists("keys.env"):
        print("❌ keys.env not found. Please make sure your environment file exists.")
        input("Press Enter to exit...")
        return
    
    print("🔄 Starting LiveKit Agent...")
    
    # Start the agent
    try:
        agent_process = subprocess.Popen([sys.executable, "main.py"])
        print(f"✅ Agent started with PID: {agent_process.pid}")
    except Exception as e:
        print(f"❌ Failed to start agent: {e}")
        input("Press Enter to exit...")
        return
    
    # Wait for agent to initialize
    print("⏳ Waiting for agent to initialize (5 seconds)...")
    time.sleep(5)
    
    # Open browser
    print("🌐 Opening LiveKit Agents Playground...")
    try:
        webbrowser.open("https://agents.livekit.io/")
        print("✅ Browser opened successfully!")
    except Exception as e:
        print(f"❌ Failed to open browser: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 SUCCESS! Your agent is now running!")
    print("=" * 50)
    print("\n📋 Next Steps:")
    print("1. In the browser window that opened:")
    print("   - Click 'Connect to Room'")
    print("   - Enter any room name (e.g., 'my-chat-room')")
    print("   - Click 'Join Room'")
    print("2. Start chatting with your AI avatar!")
    print("\n💡 Tips:")
    print("- Your agent is running in the background")
    print("- Documents will load automatically on first query")
    print("- OpenAI embeddings will initialize in the background")
    print("- The avatar will respond using OpenAI's understanding")
    print("\n🛑 To stop the agent: Press Ctrl+C")
    
    try:
        agent_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping agent...")
        agent_process.terminate()
        print("✅ Agent stopped successfully!")

if __name__ == "__main__":
    main()
