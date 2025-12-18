"""
User Onboarding Module

Handles user onboarding flow and AI-powered profile generation.

Author: Brain-Time
Project: Productivity Coach
"""

from dotenv import load_dotenv
import os
from groq import Groq
import json
from typing import Dict, Optional
from datetime import datetime

from ai_config import (
    ONBOARDING_QUESTIONS,
    get_model,
    get_temperature,
    get_language_code,
    get_language_instruction
)

load_dotenv()


# ============================================================================
# GROQ CLIENT INITIALIZATION
# ============================================================================

def get_groq_client() -> Groq:
    """Initialize and return Groq client."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables")
    return Groq(api_key=api_key)


# ============================================================================
# PROFILE GENERATION
# ============================================================================

def generate_user_profile(onboarding_data: Dict) -> Dict:
    """
    Generate personalized AI profile based on onboarding answers.
    
    Args:
        onboarding_data: Dict with user's onboarding answers
        
    Returns:
        Dict with personalized system messages and settings
    """
    client = get_groq_client()
    
    # Extract user information
    language = onboarding_data.get('language', 'English')
    role = onboarding_data.get('role', 'individual')
    goals = onboarding_data.get('goals', [])
    available_time = onboarding_data.get('available_time', 'varies')
    challenges = onboarding_data.get('challenges', 'general productivity')
    islamic_practice = onboarding_data.get('islamic_practice', 'Prefer not to say')
    motivation_style = onboarding_data.get('motivation_style', 'Mix of everything')
    
    # Get language instruction
    language_code = get_language_code(language)
    language_instruction = get_language_instruction(language_code)
    
    # Create prompt for AI
    prompt = f"""Based on this user information, create a personalized productivity coaching profile.

USER INFORMATION:
- Language: {language}
- Role: {role}
- Goals: {', '.join(goals) if isinstance(goals, list) else goals}
- Available Time: {available_time}
- Main Challenge: {challenges}
- Islamic Practice Level: {islamic_practice}
- Motivation Style: {motivation_style}

TASK:
Generate a JSON response with these fields:

1. "system_message_daily_planning": A personalized system message for daily planning (150-200 words)
   - Should address their specific role and challenges
   - Acknowledge their time constraints
   - Focus on their stated goals
   - Use appropriate Islamic references based on their practice level
   
2. "system_message_weekly_review": A personalized system message for weekly reviews (100-150 words)
   - Should focus on their motivation style
   - Encourage based on their challenges
   - Reference their goals
   
3. "coaching_tone": Best coaching tone for this user (2-3 words, e.g., "encouraging, practical")

4. "key_focus_areas": Top 3 areas to emphasize based on their goals (array of strings)

5. "time_block_size": Recommended time block size in minutes (15, 30, 45, or 60)
   - Base this on their available time and role

6. "islamic_emphasis": Level of Islamic content to include ("high", "medium", "low", "minimal")
   - Base this on their islamic_practice level

IMPORTANT: 
- {language_instruction}
- Respond ONLY with valid JSON
- No markdown, no code blocks, just pure JSON
- Make it specific to their situation"""

    try:
        response = client.chat.completions.create(
            model=get_model("onboarding"),
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert at creating personalized productivity coaching profiles. Always respond with valid JSON only, no markdown formatting."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=get_temperature("onboarding")
        )
        
        # Extract response content
        content = response.choices[0].message.content.strip()
        
        # Remove markdown code blocks if present
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
            content = content.strip()
        
        # Parse JSON
        profile = json.loads(content)
        
        # Add metadata
        profile["onboarding_data"] = onboarding_data
        profile["created_at"] = datetime.now().isoformat()
        profile["language_code"] = language_code
        
        return profile
        
    except json.JSONDecodeError as e:
        print(f"⚠️  JSON parsing failed: {e}")
        print(f"Raw response: {content[:200]}...")
        return get_default_profile(onboarding_data)
        
    except Exception as e:
        print(f"❌ Profile generation failed: {e}")
        return get_default_profile(onboarding_data)


def get_default_profile(onboarding_data: Dict) -> Dict:
    """
    Generate fallback profile if AI generation fails.
    
    Args:
        onboarding_data: User's onboarding answers
        
    Returns:
        Default profile dict
    """
    language = onboarding_data.get('language', 'English')
    language_code = get_language_code(language)
    role = onboarding_data.get('role', 'individual')
    goals = onboarding_data.get('goals', [])
    
    return {
        "system_message_daily_planning": f"""You are a productivity coach for a {role}.
        
Focus on these goals: {', '.join(goals) if isinstance(goals, list) else goals}.

Provide:
- Realistic time-blocked schedules
- Practical, actionable advice
- Encouragement and support
- Clear structure with specific times""",
        
        "system_message_weekly_review": """You are a reflective productivity coach.

Provide:
- Celebration of wins
- Pattern identification
- Constructive suggestions
- Encouragement for next week""",
        
        "coaching_tone": "encouraging, practical",
        "key_focus_areas": goals[:3] if isinstance(goals, list) else ["productivity", "balance", "growth"],
        "time_block_size": 30,
        "islamic_emphasis": "medium",
        "onboarding_data": onboarding_data,
        "created_at": datetime.now().isoformat(),
        "language_code": language_code,
        "is_default": True
    }


# ============================================================================
# PROFILE VALIDATION
# ============================================================================

def validate_profile(profile: Dict) -> bool:
    """
    Validate that profile has all required fields.
    
    Args:
        profile: Profile dict to validate
        
    Returns:
        True if valid, False otherwise
    """
    required_fields = [
        "system_message_daily_planning",
        "system_message_weekly_review",
        "coaching_tone",
        "key_focus_areas",
        "time_block_size",
        "onboarding_data"
    ]
    
    for field in required_fields:
        if field not in profile:
            print(f"⚠️  Missing required field: {field}")
            return False
    
    return True


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("ONBOARDING MODULE TEST")
    print("=" * 60)
    
    # Test with realistic user data
    test_user_data = {
        "language": "Deutsch",
        "role": "Parent with young children",
        "goals": ["Quran memorization/study", "Career development", "Family time"],
        "available_time": "1-2 hours",
        "challenges": "Finding time with kids",
        "islamic_practice": "Practicing - working on consistency",
        "motivation_style": "Mix of everything"
    }
    
    print("\n📝 Test User Data:")
    for key, value in test_user_data.items():
        print(f"   {key}: {value}")
    
    print("\n🔄 Generating personalized profile...")
    profile = generate_user_profile(test_user_data)
    
    print("\n✅ Profile Generated!\n")
    print("=" * 60)
    print("DAILY PLANNING SYSTEM MESSAGE:")
    print("=" * 60)
    print(profile.get("system_message_daily_planning", "N/A"))
    
    print("\n" + "=" * 60)
    print("WEEKLY REVIEW SYSTEM MESSAGE:")
    print("=" * 60)
    print(profile.get("system_message_weekly_review", "N/A"))
    
    print("\n" + "=" * 60)
    print("PROFILE DETAILS:")
    print("=" * 60)
    print(f"Coaching Tone: {profile.get('coaching_tone', 'N/A')}")
    print(f"Focus Areas: {', '.join(profile.get('key_focus_areas', []))}")
    print(f"Time Block Size: {profile.get('time_block_size', 'N/A')} minutes")
    print(f"Islamic Emphasis: {profile.get('islamic_emphasis', 'N/A')}")
    print(f"Language: {profile.get('language_code', 'N/A')}")
    print(f"Is Default: {profile.get('is_default', False)}")
    
    print("\n" + "=" * 60)
    print("VALIDATION:")
    print("=" * 60)
    is_valid = validate_profile(profile)
    print(f"Profile Valid: {'✅ Yes' if is_valid else '❌ No'}")
    
    print("\n✅ Test complete!")
