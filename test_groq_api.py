'''
from dotenv import load_dotenv
import os
import groq

# Load environment variables from .env file
load_dotenv()
# Access environment variables
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("GROQ_API_KEY is not set in the environment variables.")
    exit(1)

client = groq.Client(api_key=api_key)

try:

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": "Erkläre in einem Satz, was Produkitivität bedeutet.",
            }
        ]
    )

    print("AI Response: ", response.choices[0].message.content)
    print("Total Tokens Used: ", response.usage.total_tokens) 

except groq.AuthenticationError:
    print("Authentication failed. Please check your API key.")

except groq.RateLimitError:
    print("Rate limit exceeded. Please try again later.")

except groq.BadRequestError:
    print("Bad request. Please check the request parameters.")

except groq.InternalServerError:
    print("Internal server error. Please try again later.")

except Exception as e:
    print(f"An error occurred: {e}")
'''
"""
Test script for Groq API (Application Programming Interface) integration.

This script validates the API connection and demonstrates basic usage.
"""

from dotenv import load_dotenv
import os
from groq import Groq
import groq

# Constants
MODEL_NAME = "llama-3.3-70b-versatile"
TEST_PROMPT = "Explain in one sentence what productivity means."

# Load environment variables
load_dotenv()

# Validate API key
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    print("❌ GROQ_API_KEY not found in .env file!")
    print("💡 Make sure you have a .env file with: GROQ_API_KEY=your_key_here")
    exit(1)

print("✅ API key loaded successfully!")

# Initialize Groq client
client = Groq(api_key=api_key)

try:
    print(f"🤖 Testing Groq API with model: {MODEL_NAME}")
    
    # Send test request
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": TEST_PROMPT
            }
        ]
    )
    
    # Extract and display response
    ai_response = response.choices[0].message.content
    print(f"\n📝 AI Response:\n{ai_response}\n")
    
    # Display token usage
    print("📊 Token Usage:")
    print(f"   Prompt tokens: {response.usage.prompt_tokens}")
    print(f"   Completion tokens: {response.usage.completion_tokens}")
    print(f"   Total tokens: {response.usage.total_tokens}")
    
    print("\n✅ Test successful!")

except groq.AuthenticationError:
    print("❌ Authentication failed! Check your API key.")
    
except groq.RateLimitError:
    print("⏳ Rate limit exceeded! Wait a moment and try again.")
    
except groq.BadRequestError as e:
    print(f"❌ Bad request! Check your parameters: {e}")
    
except groq.InternalServerError:
    print("🔧 Server error! Try again later.")
    
except Exception as e:
    print(f"❌ Unexpected error: {e}")
