"""
AI Configuration Module

Centralized configuration for all AI interactions.
Handles models, temperatures, system messages, and personalization.

Author: Brain-Time
Project: Productivity Coach
"""

from typing import Dict, List, Optional
import json


# ============================================================================
# MODEL CONFIGURATION
# ============================================================================

MODELS = {
    "daily_planning": "llama-3.3-70b-versatile",
    "weekly_review": "llama-3.1-70b-versatile",  # Long context for week data
    "quick_task": "llama-3.1-8b-instant",
    "motivational": "llama-3.1-8b-instant",
    "onboarding": "llama-3.3-70b-versatile",  # High quality for profile generation
}


# ============================================================================
# TEMPERATURE CONFIGURATION
# ============================================================================

TEMPERATURES = {
    "daily_planning": 0.4,    # Consistent, structured output
    "weekly_review": 0.8,     # Analytical but creative suggestions
    "quick_task": 0.5,        # Practical with some variance
    "motivational": 1.1,      # Creative and inspiring
    "onboarding": 0.7,        # Balanced for profile generation
}


# ============================================================================
# TOKEN LIMITS
# ============================================================================

MAX_TOKENS = {
    "daily_planning": 500,
    "weekly_review": 600,
    "quick_task": 150,
    "motivational": 200,
    "onboarding": 800,
}


# ============================================================================
# DEFAULT SYSTEM MESSAGES (Before Personalization)
# ============================================================================

DEFAULT_SYSTEM_MESSAGES = {
    "daily_planning": """You are an Islamic productivity coach specializing in time management for busy individuals.

Your responses should:
- Create realistic, time-blocked schedules
- Prioritize spiritual growth (Quran, prayer times)
- Acknowledge real-world constraints
- Be encouraging and practical
- Format as a clear schedule with times""",

    "weekly_review": """You are a reflective productivity coach analyzing weekly progress.

Your responses should:
- Start by celebrating wins (even small ones)
- Identify patterns in productivity
- Suggest 2-3 specific adjustments for next week
- Be constructive and encouraging, never critical
- Reference principles of continuous improvement""",

    "quick_task": """You are a helpful productivity assistant for quick questions.

Keep responses:
- Brief (2-3 sentences maximum)
- Immediately actionable
- Positive and encouraging""",

    "motivational": """You are an Islamic motivational speaker focused on productivity.

Provide:
- A relevant Quranic verse or Hadith (with translation)
- Brief reflection on its meaning for productivity
- One actionable reminder
- Keep total response under 100 words""",
}


# ============================================================================
# LANGUAGE CONFIGURATION
# ============================================================================

LANGUAGES = {
    "en": {
        "name": "English",
        "code": "en",
        "ai_instruction": "Respond in English.",
        "direction": "ltr",
        "ui_strings": {
            "welcome": "Welcome to Your Productivity Coach",
            "daily_plan": "Daily Plan",
            "weekly_review": "Weekly Review",
            "settings": "Settings",
            "onboarding": "Let's Get Started",
        }
    },
    "de": {
        "name": "Deutsch",
        "code": "de",
        "ai_instruction": "Antworte auf Deutsch.",
        "direction": "ltr",
        "ui_strings": {
            "welcome": "Willkommen zu Deinem Produktivitäts-Coach",
            "daily_plan": "Tagesplan",
            "weekly_review": "Wochenrückblick",
            "settings": "Einstellungen",
            "onboarding": "Lass uns starten",
        }
    },
    "ar": {
        "name": "العربية",
        "code": "ar",
        "ai_instruction": "Respond in Arabic (العربية). Use proper Arabic script.",
        "direction": "rtl",
        "ui_strings": {
            "welcome": "مرحبا بك في مدرب الإنتاجية",
            "daily_plan": "الخطة اليومية",
            "weekly_review": "المراجعة الأسبوعية",
            "settings": "الإعدادات",
            "onboarding": "لنبدأ",
        }
    },
    "fr": {
        "name": "Français",
        "code": "fr",
        "ai_instruction": "Répondez en français.",
        "direction": "ltr",
        "ui_strings": {
            "welcome": "Bienvenue dans votre coach de productivité",
            "daily_plan": "Plan quotidien",
            "weekly_review": "Revue hebdomadaire",
            "settings": "Paramètres",
            "onboarding": "Commençons",
        }
    }
}


# ============================================================================
# ONBOARDING QUESTIONS
# ============================================================================

ONBOARDING_QUESTIONS = [
    {
        "id": "language",
        "question_en": "Which language would you like to use?",
        "question_de": "Welche Sprache möchtest du verwenden?",
        "question_ar": "ما هي اللغة التي تريد استخدامها؟",
        "type": "select",
        "options": ["English", "Deutsch", "العربية (Arabic)", "Français"],
        "required": True,
        "ai_context": "preferred_language"
    },
    {
        "id": "role",
        "question_en": "What best describes you?",
        "question_de": "Was beschreibt dich am besten?",
        "type": "select",
        "options": [
            "Parent with young children",
            "Student",
            "Working professional",
            "Entrepreneur",
            "Homemaker",
            "Other"
        ],
        "required": True,
        "ai_context": "user_role"
    },
    {
        "id": "goals",
        "question_en": "What are your main goals? (Select all that apply)",
        "question_de": "Was sind deine Hauptziele? (Wähle alle zutreffenden)",
        "type": "multiselect",
        "options": [
            "Quran memorization/study",
            "Islamic knowledge",
            "Career development",
            "Family time",
            "Personal projects",
            "Health & fitness",
            "Financial goals"
        ],
        "required": True,
        "ai_context": "primary_goals"
    },
    {
        "id": "available_time",
        "question_en": "How much focused time do you typically have per day?",
        "question_de": "Wie viel fokussierte Zeit hast du normalerweise pro Tag?",
        "type": "select",
        "options": [
            "Less than 1 hour",
            "1-2 hours",
            "2-4 hours",
            "4+ hours",
            "Varies greatly"
        ],
        "required": True,
        "ai_context": "time_availability"
    },
    {
        "id": "challenges",
        "question_en": "What's your biggest productivity challenge?",
        "question_de": "Was ist deine größte Produktivitäts-Herausforderung?",
        "type": "select",
        "options": [
            "Finding time with kids",
            "Staying consistent",
            "Prioritizing tasks",
            "Avoiding distractions",
            "Balancing multiple roles",
            "Morning routine",
            "Evening routine"
        ],
        "required": False,
        "ai_context": "main_challenge"
    },
    {
        "id": "islamic_practice",
        "question_en": "How would you describe your Islamic practice?",
        "question_de": "Wie würdest du deine islamische Praxis beschreiben?",
        "type": "select",
        "options": [
            "Beginner - learning the basics",
            "Practicing - working on consistency",
            "Committed - established routine",
            "Prefer not to say"
        ],
        "required": False,
        "ai_context": "islamic_level"
    },
    {
        "id": "motivation_style",
        "question_en": "What motivates you most?",
        "question_de": "Was motiviert dich am meisten?",
        "type": "select",
        "options": [
            "Spiritual reminders (Quran, Hadith)",
            "Practical tips and strategies",
            "Success stories",
            "Accountability and tracking",
            "Mix of everything"
        ],
        "required": False,
        "ai_context": "motivation_preference"
    }
]


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_model(feature: str) -> str:
    """Get model name for a specific feature."""
    return MODELS.get(feature, MODELS["quick_task"])


def get_temperature(feature: str) -> float:
    """Get temperature for a specific feature."""
    return TEMPERATURES.get(feature, 0.7)


def get_max_tokens(feature: str) -> int:
    """Get max tokens for a specific feature."""
    return MAX_TOKENS.get(feature, 300)


def get_system_message(feature: str) -> str:
    """Get default system message for a specific feature."""
    return DEFAULT_SYSTEM_MESSAGES.get(
        feature, 
        DEFAULT_SYSTEM_MESSAGES["quick_task"]
    )


def get_language_instruction(language_code: str) -> str:
    """Get AI instruction for responding in specific language."""
    return LANGUAGES.get(language_code, LANGUAGES["en"])["ai_instruction"]


def get_ui_string(language_code: str, key: str) -> str:
    """Get UI string in user's language."""
    lang = LANGUAGES.get(language_code, LANGUAGES["en"])
    return lang["ui_strings"].get(key, key)


def get_ai_config(feature: str, user_profile: Optional[Dict] = None) -> Dict:
    """
    Get complete AI configuration for a feature.
    
    Args:
        feature: Feature name (daily_planning, weekly_review, etc.)
        user_profile: Optional user profile for personalization
        
    Returns:
        Dict with model, temperature, system_message, max_tokens
    """
    config = {
        "model": get_model(feature),
        "temperature": get_temperature(feature),
        "max_tokens": get_max_tokens(feature),
    }
    
    # Use personalized system message if available
    if user_profile and "system_message_" + feature in user_profile:
        config["system_message"] = user_profile["system_message_" + feature]
    else:
        config["system_message"] = get_system_message(feature)
    
    # Add language instruction if user profile exists
    if user_profile and "onboarding_data" in user_profile:
        language = user_profile["onboarding_data"].get("language", "English")
        language_code = get_language_code(language)
        language_instruction = get_language_instruction(language_code)
        config["system_message"] += f"\n\nIMPORTANT: {language_instruction}"
    
    return config


def get_language_code(language_name: str) -> str:
    """Convert language name to code."""
    mapping = {
        "English": "en",
        "Deutsch": "de",
        "العربية (Arabic)": "ar",
        "Français": "fr"
    }
    return mapping.get(language_name, "en")


def create_messages(
    feature: str,
    user_input: str,
    user_profile: Optional[Dict] = None,
    conversation_history: Optional[List[Dict]] = None
) -> List[Dict]:
    """
    Create messages array for API call.
    
    Args:
        feature: Feature name
        user_input: User's current input
        user_profile: Optional user profile
        conversation_history: Optional previous messages
        
    Returns:
        List of message dicts
    """
    config = get_ai_config(feature, user_profile)
    
    messages = [
        {"role": "system", "content": config["system_message"]}
    ]
    
    # Add conversation history if provided
    if conversation_history:
        messages.extend(conversation_history)
    
    # Add current user input
    messages.append({"role": "user", "content": user_input})
    
    return messages


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("AI CONFIG MODULE TEST")
    print("=" * 60)
    
    # Test 1: Get config without profile
    print("\n1. Default Configuration:")
    config = get_ai_config("daily_planning")
    print(f"   Model: {config['model']}")
    print(f"   Temperature: {config['temperature']}")
    print(f"   Max Tokens: {config['max_tokens']}")
    print(f"   System Message: {config['system_message'][:100]}...")
    
    # Test 2: Get config with profile
    print("\n2. Personalized Configuration:")
    mock_profile = {
        "system_message_daily_planning": "You are a coach for busy parents...",
        "onboarding_data": {"language": "Deutsch"}
    }
    config = get_ai_config("daily_planning", mock_profile)
    print(f"   System Message: {config['system_message'][:100]}...")
    
    # Test 3: Create messages
    print("\n3. Messages Array:")
    messages = create_messages(
        "daily_planning",
        "I have 3 hours today",
        mock_profile
    )
    print(f"   Number of messages: {len(messages)}")
    print(f"   First message role: {messages[0]['role']}")
    
    # Test 4: Language support
    print("\n4. Language Support:")
    for lang_code, lang_data in LANGUAGES.items():
        print(f"   {lang_data['name']}: {get_ui_string(lang_code, 'welcome')}")
    
    print("\n✅ All tests passed!")
