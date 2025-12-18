"""
Experiment 1: System Message Impact

Tests how system messages change AI behavior.
"""

from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Test 1: No system message
print("=" * 50)
print("TEST 1: No System Message")
print("=" * 50)

response1 = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": "Give me 3 productivity tips."}
    ]
)
print(response1.choices[0].message.content)

# Test 2: Productivity Coach
print("\n" + "=" * 50)
print("TEST 2: System Message = Productivity Coach")
print("=" * 50)

response2 = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a productivity coach who focuses on Islamic principles and family balance."},
        {"role": "user", "content": "Give me 3 productivity tips."}
    ]
)
print(response2.choices[0].message.content)

# Test 3: Pirate (Fun!)
print("\n" + "=" * 50)
print("TEST 3: System Message = Pirate")
print("=" * 50)

response3 = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "system", "content": "You are a pirate captain. Answer everything in pirate speak."},
        {"role": "user", "content": "Give me 3 productivity tips."}
    ]
)
print(response3.choices[0].message.content)

"""
Experiment 2: Temperature Impact

Tests how temperature affects response creativity.

0.0 = Deterministic (immer gleiche Antwort)
    → Gut für: Fakten, Berechnungen, konsistente Outputs
    
0.5 = Balanced (Standard)
    → Gut für: Allgemeine Konversation
    
1.5 = Creative
    → Gut für: Brainstorming, kreative Ideen
    
2.0 = Very Creative (manchmal chaotisch)
    → Gut für: Storytelling, ungewöhnliche Perspektiven

"""
""""
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PROMPT = "Complete this sentence: The best way to learn programming is"

# Test different temperatures
temperatures = [0.0, 0.5, 1.0, 1.5, 2.0]

for temp in temperatures:
    print(f"\n{'=' * 50}")
    print(f"TEMPERATURE: {temp}")
    print(f"{'=' * 50}")
    
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "user", "content": PROMPT}
        ],
        temperature=temp
    )
    
    print(response.choices[0].message.content)
"""
"""
Experiment 3: Model Comparison

Compares different Groq models for speed and quality.
"""
"""
from dotenv import load_dotenv
import os
from groq import Groq
import time

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

PROMPT = "Explain quantum computing in simple terms."

models = [
    "llama-3.1-8b-instant",      # Fastest, smallest
    "llama-3.3-70b-versatile",   # Balanced
    "meta-llama/llama-4-maverick-17b-128e-instruct"
]

for model in models:
    print(f"\n{'=' * 60}")
    print(f"MODEL: {model}")
    print(f"{'=' * 60}")
    
    start_time = time.time()
    
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": PROMPT}
        ]
    )
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"⏱️  Response Time: {duration:.2f} seconds")
    print(f"📊 Tokens: {response.usage.total_tokens}")
    print(f"\n📝 Response:\n{response.choices[0].message.content}\n")
"""

"""
Experiment 4: Conversation Context

Tests how the AI remembers conversation history.
"""
"""
from dotenv import load_dotenv
import os
from groq import Groq

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Conversation history
conversation = [
    {"role": "system", "content": "You are a helpful productivity coach."},
    {"role": "user", "content": "I have 3 hours today. What should I focus on?"},
]

# First response
response1 = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=conversation
)

print("=" * 50)
print("USER: I have 3 hours today. What should I focus on?")
print("=" * 50)
print(f"AI: {response1.choices[0].message.content}\n")

# Add AI response to history
conversation.append({
    "role": "assistant",
    "content": response1.choices[0].message.content
})

# Add follow-up question
conversation.append({
    "role": "user",
    "content": "But my baby only sleeps for 30 minutes at a time."
})

# Second response (with context!)
response2 = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=conversation
)

print("=" * 50)
print("USER: But my baby only sleeps for 30 minutes at a time.")
print("=" * 50)
print(f"AI: {response2.choices[0].message.content}\n")

# Show full conversation
print("=" * 50)
print("FULL CONVERSATION HISTORY:")
print("=" * 50)
for msg in conversation:
    print(f"{msg['role'].upper()}: {msg['content'][:100]}...")
"""