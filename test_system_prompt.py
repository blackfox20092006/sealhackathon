"""
Demo script showing system prompt functionality
Run after starting the server: python backend/main.py
"""

import requests
import json

BASE_URL = "http://localhost:8000"


def test_with_system_prompt():
    """Test request with system prompt (to-do list context)"""
    print("\n" + "="*60)
    print("🔍 Test 1: WITH System Prompt (To-Do List)")
    print("="*60)
    
    payload = {
        "prompt": "List my to-do list",
        "model": "gpt-3.5-turbo",
        "use_system_prompt": True  # Use the SRS.txt system prompt
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Status: {response.status_code}")
            print(f"📝 Prompt: {payload['prompt']}")
            print(f"🤖 Using System Prompt: {payload['use_system_prompt']}")
            print(f"\n📋 Response:\n{data['response']}\n")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running at http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_without_system_prompt():
    """Test request without system prompt (general response)"""
    print("\n" + "="*60)
    print("🔍 Test 2: WITHOUT System Prompt (General)")
    print("="*60)
    
    payload = {
        "prompt": "Write a haiku about programming",
        "model": "gpt-3.5-turbo",
        "use_system_prompt": False  # Skip system prompt
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/generate",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Status: {response.status_code}")
            print(f"📝 Prompt: {payload['prompt']}")
            print(f"🤖 Using System Prompt: {payload['use_system_prompt']}")
            print(f"\n📋 Response:\n{data['response']}\n")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running at http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")


def test_todo_variations():
    """Test different to-do list queries with system prompt"""
    print("\n" + "="*60)
    print("🔍 Test 3: To-Do List Variations (With System Prompt)")
    print("="*60)
    
    prompts = [
        "List my to-do list",
        "Show all tasks",
        "Display tasks for today",
        "List incomplete tasks",
        "Show high priority tasks tagged 'work'"
    ]
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\n--- Query {i}/{len(prompts)} ---")
        print(f"📝 Prompt: {prompt}")
        
        payload = {
            "prompt": prompt,
            "model": "gpt-3.5-turbo",
            "use_system_prompt": True
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/api/generate",
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"📋 Response: {data['response'][:200]}...")  # Show first 200 chars
            else:
                print(f"❌ Error {response.status_code}")
        except Exception as e:
            print(f"❌ Error: {e}")
            break


def test_streaming_with_system_prompt():
    """Test streaming endpoint with system prompt"""
    print("\n" + "="*60)
    print("🔍 Test 4: Streaming WITH System Prompt")
    print("="*60)
    
    payload = {
        "prompt": "List my tasks for this week",
        "model": "gpt-3.5-turbo",
        "use_system_prompt": True
    }
    
    print(f"\n📝 Prompt: {payload['prompt']}")
    print("🌊 Streaming response:\n")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/generate/stream",
            json=payload,
            stream=True,
            timeout=30
        )
        
        for chunk in response.iter_content(chunk_size=None, decode_unicode=True):
            if chunk:
                print(chunk, end='', flush=True)
        
        print("\n")
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server. Make sure it's running at http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    print("=" * 60)
    print("🚀 System Prompt Demo")
    print("=" * 60)
    print("\nThis demo shows how system prompts work:")
    print("- With system prompt: AI follows SRS.txt instructions")
    print("- Without system prompt: AI gives general responses")
    print("\n⚠️  Make sure the server is running:")
    print("   cd backend && python main.py")
    print("=" * 60)
    
    # Check server
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        if response.status_code == 200:
            print("✅ Server is running!\n")
        else:
            print("⚠️  Server responded but with unexpected status\n")
    except:
        print("❌ Server is NOT running. Start it first!\n")
        print("Run: cd backend && python main.py")
        return
    
    # Run tests
    test_with_system_prompt()
    test_without_system_prompt()
    test_todo_variations()
    test_streaming_with_system_prompt()
    
    print("\n" + "=" * 60)
    print("✅ All tests completed!")
    print("=" * 60)
    print("\n💡 Key Takeaway:")
    print("  - use_system_prompt=True  → Uses SRS.txt context")
    print("  - use_system_prompt=False → General AI response")
    print("=" * 60)


if __name__ == "__main__":
    main()
