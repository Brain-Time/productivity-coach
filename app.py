"""
Productivity Coach - Main Application

AI-powered productivity app with personalized coaching.

Author: Brain-Time
Project: Productivity Coach
"""

import streamlit as st
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os
from groq import Groq

# Import our modules
from ai_config import (
    ONBOARDING_QUESTIONS,
    LANGUAGES,
    get_ai_config,
    get_language_code,
    get_ui_string,
    create_messages
)
from onboarding import generate_user_profile, validate_profile
from database import (
    init_database,
    save_user_profile,
    get_active_user_profile,
    save_daily_plan,
    get_daily_plan,
    get_recent_daily_plans,
    save_weekly_review,
    get_all_weekly_reviews,
    get_database_stats,
    reset_database
)

# Load environment variables
load_dotenv()


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================

st.set_page_config(
    page_title="Productivity Coach",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================================
# CUSTOM CSS
# ============================================================================

def inject_custom_css():
    """Inject custom CSS for better styling."""
    st.markdown("""
    <style>
    /* Better spacing */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* Better buttons */
    .stButton button {
        border-radius: 8px;
        font-weight: 500;
    }
    
    /* Plan content styling */
    .plan-content {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
        margin: 1rem 0;
    }
    
    /* RTL support for Arabic */
    [dir="rtl"] {
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)


# ============================================================================
# SESSION STATE INITIALIZATION
# ============================================================================

def init_session_state():
    """Initialize session state variables."""
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = None
    
    if 'onboarding_complete' not in st.session_state:
        st.session_state.onboarding_complete = False
    
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'daily_planning'
    
    if 'language' not in st.session_state:
        st.session_state.language = 'en'
    
    if 'show_plan_code' not in st.session_state:
        st.session_state.show_plan_code = False


# ============================================================================
# GROQ CLIENT
# ============================================================================

@st.cache_resource
def get_groq_client():
    """Get cached Groq client."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("❌ GROQ_API_KEY not found in .env file!")
        st.stop()
    return Groq(api_key=api_key)


# ============================================================================
# LANGUAGE STRINGS
# ============================================================================

UI_STRINGS = {
    'en': {
        'welcome_title': '🎯 Welcome to Your Productivity Coach',
        'welcome_subtitle': "Let's personalize your experience!",
        'welcome_description': 'Answer a few questions so I can tailor the coaching to your unique situation. This will take about **2 minutes**.',
        'q1_title': '1️⃣ Language / Sprache / اللغة',
        'q1_label': 'Which language would you like to use?',
        'q2_title': '2️⃣ Your Role',
        'q2_label': 'What best describes you?',
        'q3_title': '3️⃣ Your Goals',
        'q3_label': 'What are your main goals? (Select all that apply)',
        'q4_title': '4️⃣ Available Time',
        'q4_label': 'How much focused time do you typically have per day?',
        'q5_title': '5️⃣ Main Challenge',
        'q5_label': "What's your biggest productivity challenge?",
        'q6_title': '6️⃣ Islamic Practice (Optional)',
        'q6_label': 'How would you describe your Islamic practice?',
        'q7_title': '7️⃣ Motivation Style',
        'q7_label': 'What motivates you most?',
        'submit_btn': '🚀 Generate My Personalized Profile',
        'generating': '🤖 AI is creating your personalized coaching profile...',
        'success': '✅ Profile created successfully!',
        'error_goals': '❌ Please select at least one goal!',
        'preview_title': '👀 Preview Your Profile',
        'preview_tone': '**Coaching Tone:**',
        'preview_focus': '**Focus Areas:**',
        'preview_timeblock': '**Time Block Size:**',
        'preview_language': '**Language:**',
    },
    'de': {
        'welcome_title': '🎯 Willkommen bei deinem Productivity Coach',
        'welcome_subtitle': 'Lass uns deine Erfahrung personalisieren!',
        'welcome_description': 'Beantworte ein paar Fragen, damit ich das Coaching auf deine einzigartige Situation zuschneiden kann. Das dauert etwa **2 Minuten**.',
        'q1_title': '1️⃣ Sprache / Language / اللغة',
        'q1_label': 'Welche Sprache möchtest du verwenden?',
        'q2_title': '2️⃣ Deine Rolle',
        'q2_label': 'Was beschreibt dich am besten?',
        'q3_title': '3️⃣ Deine Ziele',
        'q3_label': 'Was sind deine Hauptziele? (Wähle alle zutreffenden)',
        'q4_title': '4️⃣ Verfügbare Zeit',
        'q4_label': 'Wie viel konzentrierte Zeit hast du normalerweise pro Tag?',
        'q5_title': '5️⃣ Hauptherausforderung',
        'q5_label': 'Was ist deine größte Produktivitätsherausforderung?',
        'q6_title': '6️⃣ Islamische Praxis (Optional)',
        'q6_label': 'Wie würdest du deine islamische Praxis beschreiben?',
        'q7_title': '7️⃣ Motivationsstil',
        'q7_label': 'Was motiviert dich am meisten?',
        'submit_btn': '🚀 Mein personalisiertes Profil erstellen',
        'generating': '🤖 KI erstellt dein personalisiertes Coaching-Profil...',
        'success': '✅ Profil erfolgreich erstellt!',
        'error_goals': '❌ Bitte wähle mindestens ein Ziel aus!',
        'preview_title': '👀 Vorschau deines Profils',
        'preview_tone': '**Coaching-Ton:**',
        'preview_focus': '**Schwerpunkte:**',
        'preview_timeblock': '**Zeitblockgröße:**',
        'preview_language': '**Sprache:**',
    },
    'ar': {
        'welcome_title': '🎯 مرحباً بك في مدرب الإنتاجية الخاص بك',
        'welcome_subtitle': 'دعنا نخصص تجربتك!',
        'welcome_description': 'أجب عن بعض الأسئلة حتى أتمكن من تخصيص التدريب لحالتك الفريدة. سيستغرق هذا حوالي **دقيقتين**.',
        'q1_title': '1️⃣ اللغة / Language / Sprache',
        'q1_label': 'أي لغة تريد استخدامها؟',
        'q2_title': '2️⃣ دورك',
        'q2_label': 'ما الذي يصفك بشكل أفضل؟',
        'q3_title': '3️⃣ أهدافك',
        'q3_label': 'ما هي أهدافك الرئيسية؟ (اختر كل ما ينطبق)',
        'q4_title': '4️⃣ الوقت المتاح',
        'q4_label': 'كم من الوقت المركز لديك عادة في اليوم؟',
        'q5_title': '5️⃣ التحدي الرئيسي',
        'q5_label': 'ما هو أكبر تحدي إنتاجية لديك؟',
        'q6_title': '6️⃣ الممارسة الإسلامية (اختياري)',
        'q6_label': 'كيف تصف ممارستك الإسلامية؟',
        'q7_title': '7️⃣ أسلوب التحفيز',
        'q7_label': 'ما الذي يحفزك أكثر؟',
        'submit_btn': '🚀 إنشاء ملفي الشخصي المخصص',
        'generating': '🤖 الذكاء الاصطناعي يقوم بإنشاء ملف التدريب المخصص الخاص بك...',
        'success': '✅ تم إنشاء الملف الشخصي بنجاح!',
        'error_goals': '❌ يرجى اختيار هدف واحد على الأقل!',
        'preview_title': '👀 معاينة ملفك الشخصي',
        'preview_tone': '**نبرة التدريب:**',
        'preview_focus': '**مجالات التركيز:**',
        'preview_timeblock': '**حجم كتلة الوقت:**',
        'preview_language': '**اللغة:**',
    },
    'fr': {
        'welcome_title': '🎯 Bienvenue dans votre Coach de Productivité',
        'welcome_subtitle': 'Personnalisons votre expérience!',
        'welcome_description': 'Répondez à quelques questions pour que je puisse adapter le coaching à votre situation unique. Cela prendra environ **2 minutes**.',
        'q1_title': '1️⃣ Langue / Language / Sprache',
        'q1_label': 'Quelle langue souhaitez-vous utiliser?',
        'q2_title': '2️⃣ Votre Rôle',
        'q2_label': 'Qu\'est-ce qui vous décrit le mieux?',
        'q3_title': '3️⃣ Vos Objectifs',
        'q3_label': 'Quels sont vos principaux objectifs? (Sélectionnez tous ceux qui s\'appliquent)',
        'q4_title': '4️⃣ Temps Disponible',
        'q4_label': 'Combien de temps concentré avez-vous généralement par jour?',
        'q5_title': '5️⃣ Défi Principal',
        'q5_label': 'Quel est votre plus grand défi de productivité?',
        'q6_title': '6️⃣ Pratique Islamique (Optionnel)',
        'q6_label': 'Comment décririez-vous votre pratique islamique?',
        'q7_title': '7️⃣ Style de Motivation',
        'q7_label': 'Qu\'est-ce qui vous motive le plus?',
        'submit_btn': '🚀 Générer Mon Profil Personnalisé',
        'generating': '🤖 L\'IA crée votre profil de coaching personnalisé...',
        'success': '✅ Profil créé avec succès!',
        'error_goals': '❌ Veuillez sélectionner au moins un objectif!',
        'preview_title': '👀 Aperçu de Votre Profil',
        'preview_tone': '**Ton du Coaching:**',
        'preview_focus': '**Domaines de Focus:**',
        'preview_timeblock': '**Taille du Bloc de Temps:**',
        'preview_language': '**Langue:**',
    }
}

DAILY_PLANNING_STRINGS = {
    'en': {
        'title': '📅 Daily Plan',
        'select_date': 'Select date:',
        'available_hours': 'Available hours:',
        'plan_exists': '📋 Plan already exists for',
        'regenerate': '🔄 Regenerate Plan',
        'add_context': '➕ Add Additional Context (Optional)',
        'context_label': 'Any specific priorities or constraints for today?',
        'context_placeholder': 'e.g., Doctor appointment at 2pm, need to finish project X',
        'generate_btn': '✨ Generate Daily Plan',
        'generating': '🤖 AI is creating your personalized plan...',
        'success': '✅ Plan generated!',
        'copy_btn': '📋 Copy to Clipboard',
        'prompt_template': """I have {hours} hours available today ({date}).

My focus areas: {focus}
Preferred time blocks: {blocks} minutes

{context}

Please create a realistic, time-blocked schedule for today."""
    },
    'de': {
        'title': '📅 Tagesplan',
        'select_date': 'Datum wählen:',
        'available_hours': 'Verfügbare Stunden:',
        'plan_exists': '📋 Plan existiert bereits für',
        'regenerate': '🔄 Plan neu generieren',
        'add_context': '➕ Zusätzlicher Kontext (Optional)',
        'context_label': 'Spezifische Prioritäten oder Einschränkungen für heute?',
        'context_placeholder': 'z.B. Arzttermin um 14 Uhr, muss Projekt X fertigstellen',
        'generate_btn': '✨ Tagesplan erstellen',
        'generating': '🤖 KI erstellt deinen personalisierten Plan...',
        'success': '✅ Plan erstellt!',
        'copy_btn': '📋 In Zwischenablage kopieren',
        'prompt_template': """Ich habe heute {hours} Stunden verfügbar ({date}).

Meine Schwerpunkte: {focus}
Bevorzugte Zeitblöcke: {blocks} Minuten

{context}

Bitte erstelle einen realistischen, zeitlich strukturierten Plan für heute."""
    },
    'ar': {
        'title': '📅 الخطة اليومية',
        'select_date': 'اختر التاريخ:',
        'available_hours': 'الساعات المتاحة:',
        'plan_exists': '📋 الخطة موجودة بالفعل لـ',
        'regenerate': '🔄 إعادة إنشاء الخطة',
        'add_context': '➕ إضافة سياق إضافي (اختياري)',
        'context_label': 'أي أولويات أو قيود محددة لهذا اليوم؟',
        'context_placeholder': 'مثال: موعد طبيب الساعة 2 مساءً، يجب إنهاء المشروع X',
        'generate_btn': '✨ إنشاء الخطة اليومية',
        'generating': '🤖 الذكاء الاصطناعي يقوم بإنشاء خطتك المخصصة...',
        'success': '✅ تم إنشاء الخطة!',
        'copy_btn': '📋 نسخ إلى الحافظة',
        'prompt_template': """لدي {hours} ساعات متاحة اليوم ({date}).

مجالات التركيز: {focus}
كتل الوقت المفضلة: {blocks} دقيقة

{context}

يرجى إنشاء جدول واقعي ومنظم زمنياً لهذا اليوم."""
    },
    'fr': {
        'title': '📅 Plan Quotidien',
        'select_date': 'Sélectionner la date:',
        'available_hours': 'Heures disponibles:',
        'plan_exists': '📋 Le plan existe déjà pour',
        'regenerate': '🔄 Régénérer le plan',
        'add_context': '➕ Ajouter un contexte supplémentaire (Optionnel)',
        'context_label': 'Des priorités ou contraintes spécifiques pour aujourd\'hui?',
        'context_placeholder': 'ex: Rendez-vous médecin à 14h, besoin de finir projet X',
        'generate_btn': '✨ Générer le plan quotidien',
        'generating': '🤖 L\'IA crée votre plan personnalisé...',
        'success': '✅ Plan généré!',
        'copy_btn': '📋 Copier dans le presse-papiers',
        'prompt_template': """J'ai {hours} heures disponibles aujourd'hui ({date}).

Mes domaines prioritaires: {focus}
Blocs de temps préférés: {blocks} minutes

{context}

Veuillez créer un emploi du temps réaliste et structuré pour aujourd'hui."""
    }
}

WEEKLY_REVIEW_STRINGS = {
    'en': {
        'title': '📊 Weekly Review',
        'week_info': '📅 Reviewing week:',
        'no_plans': '⚠️ No daily plans found for this week. Create some plans first!',
        'plans_summary': '📋 This Week\'s Plans',
        'reflections_title': '💭 Your Reflections (Optional)',
        'reflections_label': 'How did this week go? Any wins or challenges?',
        'reflections_placeholder': 'e.g., Completed Quran goal 3 days, struggled with morning routine',
        'generate_btn': '✨ Generate Weekly Review',
        'generating': '🤖 AI is analyzing your week...',
        'success': '✅ Review generated!',
    },
    'de': {
        'title': '📊 Wochenrückblick',
        'week_info': '📅 Woche im Rückblick:',
        'no_plans': '⚠️ Keine Tagespläne für diese Woche gefunden. Erstelle zuerst einige Pläne!',
        'plans_summary': '📋 Pläne dieser Woche',
        'reflections_title': '💭 Deine Reflexionen (Optional)',
        'reflections_label': 'Wie lief diese Woche? Erfolge oder Herausforderungen?',
        'reflections_placeholder': 'z.B. Quran-Ziel an 3 Tagen erreicht, Probleme mit Morgenroutine',
        'generate_btn': '✨ Wochenrückblick erstellen',
        'generating': '🤖 KI analysiert deine Woche...',
        'success': '✅ Rückblick erstellt!',
    },
    'ar': {
        'title': '📊 المراجعة الأسبوعية',
        'week_info': '📅 مراجعة الأسبوع:',
        'no_plans': '⚠️ لم يتم العثور على خطط يومية لهذا الأسبوع. قم بإنشاء بعض الخطط أولاً!',
        'plans_summary': '📋 خطط هذا الأسبوع',
        'reflections_title': '💭 تأملاتك (اختياري)',
        'reflections_label': 'كيف سار هذا الأسبوع؟ أي انتصارات أو تحديات؟',
        'reflections_placeholder': 'مثال: أكملت هدف القرآن 3 أيام، واجهت صعوبة مع روتين الصباح',
        'generate_btn': '✨ إنشاء المراجعة الأسبوعية',
        'generating': '🤖 الذكاء الاصطناعي يحلل أسبوعك...',
        'success': '✅ تم إنشاء المراجعة!',
    },
    'fr': {
        'title': '📊 Revue Hebdomadaire',
        'week_info': '📅 Révision de la semaine:',
        'no_plans': '⚠️ Aucun plan quotidien trouvé pour cette semaine. Créez d\'abord quelques plans!',
        'plans_summary': '📋 Plans de Cette Semaine',
        'reflections_title': '💭 Vos Réflexions (Optionnel)',
        'reflections_label': 'Comment s\'est passée cette semaine? Des victoires ou défis?',
        'reflections_placeholder': 'ex: Objectif Coran complété 3 jours, difficulté avec routine matinale',
        'generate_btn': '✨ Générer la Revue Hebdomadaire',
        'generating': '🤖 L\'IA analyse votre semaine...',
        'success': '✅ Revue générée!',
    }
}

SETTINGS_STRINGS = {
    'en': {
        'title': '⚙️ Settings',
        'profile_title': '👤 Your Profile',
        'language': '**Language:**',
        'coaching_tone': '**Coaching Tone:**',
        'time_block': '**Time Block Size:**',
        'focus_areas': '**Focus Areas:**',
        'onboarding_title': '📋 Onboarding Answers',
        'stats_title': '📊 Statistics',
        'daily_plans': 'Daily Plans',
        'weekly_reviews': 'Weekly Reviews',
        'db_size': 'Database Size',
        'actions_title': '🔧 Actions',
        'redo_onboarding': '🔄 Redo Onboarding',
        'reset_data': '🗑️ Reset All Data',
        'reset_confirm': '⚠️ I understand this will delete all data',
        'reset_success': '✅ Database reset! Refresh the page.',
    },
    'de': {
        'title': '⚙️ Einstellungen',
        'profile_title': '👤 Dein Profil',
        'language': '**Sprache:**',
        'coaching_tone': '**Coaching-Ton:**',
        'time_block': '**Zeitblockgröße:**',
        'focus_areas': '**Schwerpunkte:**',
        'onboarding_title': '📋 Onboarding-Antworten',
        'stats_title': '📊 Statistiken',
        'daily_plans': 'Tagespläne',
        'weekly_reviews': 'Wochenrückblicke',
        'db_size': 'Datenbankgröße',
        'actions_title': '🔧 Aktionen',
        'redo_onboarding': '🔄 Onboarding wiederholen',
        'reset_data': '🗑️ Alle Daten zurücksetzen',
        'reset_confirm': '⚠️ Ich verstehe, dass dies alle Daten löscht',
        'reset_success': '✅ Datenbank zurückgesetzt! Seite aktualisieren.',
    },
    'ar': {
        'title': '⚙️ الإعدادات',
        'profile_title': '👤 ملفك الشخصي',
        'language': '**اللغة:**',
        'coaching_tone': '**نبرة التدريب:**',
        'time_block': '**حجم كتلة الوقت:**',
        'focus_areas': '**مجالات التركيز:**',
        'onboarding_title': '📋 إجابات التسجيل',
        'stats_title': '📊 الإحصائيات',
        'daily_plans': 'الخطط اليومية',
        'weekly_reviews': 'المراجعات الأسبوعية',
        'db_size': 'حجم قاعدة البيانات',
        'actions_title': '🔧 الإجراءات',
        'redo_onboarding': '🔄 إعادة التسجيل',
        'reset_data': '🗑️ إعادة تعيين جميع البيانات',
        'reset_confirm': '⚠️ أفهم أن هذا سيحذف جميع البيانات',
        'reset_success': '✅ تم إعادة تعيين قاعدة البيانات! قم بتحديث الصفحة.',
    },
    'fr': {
        'title': '⚙️ Paramètres',
        'profile_title': '👤 Votre Profil',
        'language': '**Langue:**',
        'coaching_tone': '**Ton du Coaching:**',
        'time_block': '**Taille du Bloc de Temps:**',
        'focus_areas': '**Domaines de Focus:**',
        'onboarding_title': '📋 Réponses d\'Intégration',
        'stats_title': '📊 Statistiques',
        'daily_plans': 'Plans Quotidiens',
        'weekly_reviews': 'Revues Hebdomadaires',
        'db_size': 'Taille de la Base de Données',
        'actions_title': '🔧 Actions',
        'redo_onboarding': '🔄 Refaire l\'Intégration',
        'reset_data': '🗑️ Réinitialiser Toutes les Données',
        'reset_confirm': '⚠️ Je comprends que cela supprimera toutes les données',
        'reset_success': '✅ Base de données réinitialisée! Actualisez la page.',
    }
}


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_strings(lang_code: str, category: str) -> dict:
    """Get UI strings for a specific language and category."""
    string_maps = {
        'onboarding': UI_STRINGS,
        'daily_planning': DAILY_PLANNING_STRINGS,
        'weekly_review': WEEKLY_REVIEW_STRINGS,
        'settings': SETTINGS_STRINGS
    }
    
    strings = string_maps.get(category, UI_STRINGS)
    return strings.get(lang_code, strings['en'])


# ============================================================================
# ONBOARDING FLOW
# ============================================================================

def show_onboarding():
    """Display onboarding flow."""
    # Default to English for onboarding start
    lang_code = st.session_state.get('language', 'en')
    s = get_strings(lang_code, 'onboarding')
    
    st.title(s['welcome_title'])
    st.markdown("---")
    
    st.markdown(f"""
    ### {s['welcome_subtitle']}
    
    {s['welcome_description']}
    """)
    
    st.markdown("---")
    
    # Collect answers
    answers = {}
    
    # Question 1: Language (most important)
    st.subheader(s['q1_title'])
    language_options = [lang["name"] for lang in LANGUAGES.values()]
    answers['language'] = st.selectbox(
        s['q1_label'],
        options=language_options,
        key="q_language"
    )
    
    # Get language code for UI strings
    lang_code = get_language_code(answers['language'])
    st.session_state.language = lang_code
    s = get_strings(lang_code, 'onboarding')  # Update strings
    
    st.markdown("---")
    
    # Question 2: Role
    st.subheader(s['q2_title'])
    answers['role'] = st.selectbox(
        s['q2_label'],
        options=[
            "Parent with young children",
            "Student",
            "Working professional",
            "Entrepreneur",
            "Homemaker",
            "Other"
        ],
        key="q_role"
    )
    
    st.markdown("---")
    
    # Question 3: Goals (multiselect)
    st.subheader(s['q3_title'])
    answers['goals'] = st.multiselect(
        s['q3_label'],
        options=[
            "Quran memorization/study",
            "Islamic knowledge",
            "Career development",
            "Family time",
            "Personal projects",
            "Health & fitness",
            "Financial goals"
        ],
        key="q_goals"
    )
    
    st.markdown("---")
    
    # Question 4: Available Time
    st.subheader(s['q4_title'])
    answers['available_time'] = st.selectbox(
        s['q4_label'],
        options=[
            "Less than 1 hour",
            "1-2 hours",
            "2-4 hours",
            "4+ hours",
            "Varies greatly"
        ],
        key="q_time"
    )
    
    st.markdown("---")
    
    # Question 5: Challenges
    st.subheader(s['q5_title'])
    answers['challenges'] = st.selectbox(
        s['q5_label'],
        options=[
            "Finding time with kids",
            "Staying consistent",
            "Prioritizing tasks",
            "Avoiding distractions",
            "Balancing multiple roles",
            "Morning routine",
            "Evening routine"
        ],
        key="q_challenge"
    )
    
    st.markdown("---")
    
    # Question 6: Islamic Practice (optional)
    st.subheader(s['q6_title'])
    answers['islamic_practice'] = st.selectbox(
        s['q6_label'],
        options=[
            "Beginner - learning the basics",
            "Practicing - working on consistency",
            "Committed - established routine",
            "Prefer not to say"
        ],
        key="q_islamic"
    )
    
    st.markdown("---")
    
    # Question 7: Motivation Style
    st.subheader(s['q7_title'])
    answers['motivation_style'] = st.selectbox(
        s['q7_label'],
        options=[
            "Spiritual reminders (Quran, Hadith)",
            "Practical tips and strategies",
            "Success stories",
            "Accountability and tracking",
            "Mix of everything"
        ],
        key="q_motivation"
    )
    
    st.markdown("---")
    
    # Submit button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button(s['submit_btn'], type="primary", use_container_width=True):
            # Validate required fields
            if not answers.get('goals'):
                st.error(s['error_goals'])
                return
            
            # Generate profile
            with st.spinner(s['generating']):
                profile = generate_user_profile(answers)
                
                # Validate profile
                if validate_profile(profile):
                    # Save to database
                    user_id = save_user_profile(profile)
                    profile['db_id'] = user_id
                    
                    # Update session state
                    st.session_state.user_profile = profile
                    st.session_state.onboarding_complete = True
                    
                    st.success(s['success'])
                    st.balloons()
                    
                    # Show preview
                    with st.expander(s['preview_title']):
                        st.markdown(f"{s['preview_tone']} {profile.get('coaching_tone')}")
                        st.markdown(f"{s['preview_focus']} {', '.join(profile.get('key_focus_areas', []))}")
                        st.markdown(f"{s['preview_timeblock']} {profile.get('time_block_size')} minutes")
                        st.markdown(f"{s['preview_language']} {profile.get('language_code')}")
                    
                    st.rerun()
                else:
                    st.error("❌ Profile generation failed. Please try again.")


# ============================================================================
# DAILY PLANNING PAGE
# ============================================================================

def show_daily_planning():
    """Display daily planning interface."""
    profile = st.session_state.user_profile
    lang_code = profile.get('language_code', 'en')
    s = get_strings(lang_code, 'daily_planning')
    
    st.title(s['title'])
    st.markdown("---")
    
    # Date selection
    col1, col2 = st.columns([2, 1])
    with col1:
        selected_date = st.date_input(
            s['select_date'],
            value=datetime.now().date(),
            key="daily_plan_date"
        )
    
    with col2:
        available_hours = st.number_input(
            s['available_hours'],
            min_value=0.5,
            max_value=16.0,
            value=3.0,
            step=0.5,
            key="available_hours"
        )
    
    st.markdown("---")
    
    # Check if plan exists for this date
    date_str = selected_date.isoformat()
    existing_plan = get_daily_plan(profile['db_id'], date_str)
    
    if existing_plan:
        st.info(f"{s['plan_exists']} {date_str}")
        
        # Display plan in a nice container
        st.markdown('<div class="plan-content">', unsafe_allow_html=True)
        st.markdown(existing_plan['plan_content'])
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Regenerate button
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button(s['regenerate'], use_container_width=True):
                # Delete existing plan and regenerate
                existing_plan = None
                st.rerun()
        
        with col2:
            # Copy button (shows code view)
            if st.button(s['copy_btn'], use_container_width=True):
                st.session_state.show_plan_code = not st.session_state.get('show_plan_code', False)
                st.rerun()
        
        # Show copyable text if requested
        if st.session_state.get('show_plan_code', False):
            st.code(existing_plan['plan_content'], language=None)
    
    if not existing_plan:
        # Additional context (optional)
        with st.expander(s['add_context']):
            additional_context = st.text_area(
                s['context_label'],
                placeholder=s['context_placeholder'],
                key="additional_context"
            )
        
        # Generate plan button
        if st.button(s['generate_btn'], type="primary", use_container_width=True):
            with st.spinner(s['generating']):
                # Build prompt
                focus_areas = profile.get('key_focus_areas', [])
                time_block = profile.get('time_block_size', 30)
                
                context_text = f"\nZusätzlicher Kontext: {additional_context}" if additional_context else ""
                
                user_input = s['prompt_template'].format(
                    hours=available_hours,
                    date=date_str,
                    focus=', '.join(focus_areas),
                    blocks=time_block,
                    context=context_text
                )
                
                # Create messages
                messages = create_messages(
                    feature="daily_planning",
                    user_input=user_input,
                    user_profile=profile
                )
                
                # Get AI config
                config = get_ai_config("daily_planning", profile)
                
                # Call AI
                client = get_groq_client()
                response = client.chat.completions.create(
                    model=config['model'],
                    messages=messages,
                    temperature=config['temperature'],
                    max_tokens=config['max_tokens']
                )
                
                plan_content = response.choices[0].message.content
                
                # Save to database
                save_daily_plan(
                    user_id=profile['db_id'],
                    date=date_str,
                    plan_content=plan_content,
                    available_hours=available_hours
                )
                
                st.success(s['success'])
                st.rerun()  # Reload to show the plan


# ============================================================================
# WEEKLY REVIEW PAGE
# ============================================================================

def show_weekly_review():
    """Display weekly review interface."""
    profile = st.session_state.user_profile
    lang_code = profile.get('language_code', 'en')
    s = get_strings(lang_code, 'weekly_review')
    
    st.title(s['title'])
    st.markdown("---")
    
    # Week selection
    today = datetime.now().date()
    week_start = today - timedelta(days=today.weekday())  # Monday
    week_end = week_start + timedelta(days=6)  # Sunday
    
    st.info(f"{s['week_info']} {week_start} to {week_end}")
    
    # Get recent plans
    recent_plans = get_recent_daily_plans(profile['db_id'], limit=7)
    
    if not recent_plans:
        st.warning(s['no_plans'])
        return
    
    # Display plans summary
    with st.expander(s['plans_summary']):
        for plan in recent_plans:
            st.markdown(f"**{plan['date']}** ({plan['available_hours']}h)")
            st.markdown(plan['plan_content'][:200] + "...")
            st.markdown("---")
    
    # Review input
    st.subheader(s['reflections_title'])
    user_reflections = st.text_area(
        s['reflections_label'],
        placeholder=s['reflections_placeholder'],
        key="user_reflections"
    )
    
    # Generate review button
    if st.button(s['generate_btn'], type="primary", use_container_width=True):
        with st.spinner(s['generating']):
            # Build prompt
            plans_summary = "\n\n".join([
                f"**{p['date']}**: {p['plan_content'][:300]}"
                for p in recent_plans
            ])
            
            user_input = f"""Here are my daily plans from this week:

{plans_summary}

{f"My reflections: {user_reflections}" if user_reflections else ""}

Please provide:
1. Celebration of wins (even small ones)
2. Patterns you notice
3. 2-3 specific suggestions for next week
4. Encouragement and motivation"""
            
            # Create messages
            messages = create_messages(
                feature="weekly_review",
                user_input=user_input,
                user_profile=profile
            )
            
            # Get AI config
            config = get_ai_config("weekly_review", profile)
            
            # Call AI
            client = get_groq_client()
            response = client.chat.completions.create(
                model=config['model'],
                messages=messages,
                temperature=config['temperature'],
                max_tokens=config['max_tokens']
            )
            
            review_content = response.choices[0].message.content
            
            # Save to database
            save_weekly_review(
                user_id=profile['db_id'],
                week_start=week_start.isoformat(),
                week_end=week_end.isoformat(),
                review_content=review_content
            )
            
            st.success(s['success'])
            st.markdown("---")
            st.markdown(review_content)


# ============================================================================
# SETTINGS PAGE
# ============================================================================

def show_settings():
    """Display settings and profile management."""
    profile = st.session_state.user_profile
    lang_code = profile.get('language_code', 'en')
    s = get_strings(lang_code, 'settings')
    
    st.title(s['title'])
    st.markdown("---")
    
    # Profile information
    st.subheader(s['profile_title'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"{s['language']} {profile.get('language_code', 'N/A')}")
        st.markdown(f"{s['coaching_tone']} {profile.get('coaching_tone', 'N/A')}")
        st.markdown(f"{s['time_block']} {profile.get('time_block_size', 'N/A')} min")
    
    with col2:
        focus_areas = profile.get('key_focus_areas', [])
        st.markdown(s['focus_areas'])
        for area in focus_areas:
            st.markdown(f"- {area}")
    
    st.markdown("---")
    
    # Onboarding data
    with st.expander(s['onboarding_title']):
        onboarding_data = profile.get('onboarding_data', {})
        for key, value in onboarding_data.items():
            st.markdown(f"**{key}:** {value}")
    
    st.markdown("---")
    
    # Database stats
    st.subheader(s['stats_title'])
    stats = get_database_stats()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(s['daily_plans'], stats['total_daily_plans'])
    with col2:
        st.metric(s['weekly_reviews'], stats['total_weekly_reviews'])
    with col3:
        st.metric(s['db_size'], f"{stats['db_size_kb']} KB")
    
    st.markdown("---")
    
    # Actions
    st.subheader(s['actions_title'])
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(s['redo_onboarding'], use_container_width=True):
            st.session_state.onboarding_complete = False
            st.session_state.user_profile = None
            st.rerun()
    
    with col2:
        if st.button(s['reset_data'], use_container_width=True):
            if st.checkbox(s['reset_confirm']):
                reset_database()
                st.session_state.onboarding_complete = False
                st.session_state.user_profile = None
                st.success(s['reset_success'])
                st.rerun()


# ============================================================================
# SIDEBAR
# ============================================================================

def show_sidebar():
    """Display sidebar navigation."""
    with st.sidebar:
        st.title("🎯 Productivity Coach")
        st.markdown("---")
        
        # Navigation
        if st.session_state.onboarding_complete:
            profile = st.session_state.user_profile
            lang_code = profile.get('language_code', 'en')
            
            # Welcome message
            welcome_messages = {
                'en': '👋 Welcome back!',
                'de': '👋 Willkommen zurück!',
                'ar': '👋 مرحباً بعودتك!',
                'fr': '👋 Bon retour!'
            }
            st.markdown(welcome_messages.get(lang_code, welcome_messages['en']))
            st.markdown(f"🌍 Language: {lang_code.upper()}")
            st.markdown("---")
            
            # Menu
            menu_options = {
                'en': {
                    "📅 Daily Planning": "daily_planning",
                    "📊 Weekly Review": "weekly_review",
                    "⚙️ Settings": "settings"
                },
                'de': {
                    "📅 Tagesplanung": "daily_planning",
                    "📊 Wochenrückblick": "weekly_review",
                    "⚙️ Einstellungen": "settings"
                },
                'ar': {
                    "📅 التخطيط اليومي": "daily_planning",
                    "📊 المراجعة الأسبوعية": "weekly_review",
                    "⚙️ الإعدادات": "settings"
                },
                'fr': {
                    "📅 Planification Quotidienne": "daily_planning",
                    "📊 Revue Hebdomadaire": "weekly_review",
                    "⚙️ Paramètres": "settings"
                }
            }
            
            menu = menu_options.get(lang_code, menu_options['en'])
            
            for label, page in menu.items():
                if st.button(label, use_container_width=True):
                    st.session_state.current_page = page
                    st.rerun()
            
            st.markdown("---")
            
            # Quick stats
            stats = get_database_stats()
            stats_labels = {
                'en': {'plans': 'Plans:', 'reviews': 'Reviews:'},
                'de': {'plans': 'Pläne:', 'reviews': 'Rückblicke:'},
                'ar': {'plans': 'الخطط:', 'reviews': 'المراجعات:'},
                'fr': {'plans': 'Plans:', 'reviews': 'Revues:'}
            }
            labels = stats_labels.get(lang_code, stats_labels['en'])
            
            st.markdown("### 📈 Quick Stats")
            st.markdown(f"{labels['plans']} {stats['total_daily_plans']}")
            st.markdown(f"{labels['reviews']} {stats['total_weekly_reviews']}")
        
        else:
            info_messages = {
                'en': '👋 Complete onboarding to get started!',
                'de': '👋 Schließe das Onboarding ab, um zu starten!',
                'ar': '👋 أكمل التسجيل للبدء!',
                'fr': '👋 Complétez l\'intégration pour commencer!'
            }
            lang = st.session_state.get('language', 'en')
            st.info(info_messages.get(lang, info_messages['en']))
        
        st.markdown("---")
        st.markdown("Built with ❤️ by [Brain-Time](https://github.com/Brain-Time)")


# ============================================================================
# MAIN APP
# ============================================================================

def main():
    """Main application entry point."""
    # Inject custom CSS
    inject_custom_css()
    
    # Initialize
    init_database()
    init_session_state()
    
    # Check for existing user profile
    if not st.session_state.user_profile:
        existing_profile = get_active_user_profile()
        if existing_profile:
            st.session_state.user_profile = existing_profile
            st.session_state.onboarding_complete = True
    
    # Show sidebar
    show_sidebar()
    
    # Route to appropriate page
    if not st.session_state.onboarding_complete:
        show_onboarding()
    else:
        page = st.session_state.current_page
        
        if page == 'daily_planning':
            show_daily_planning()
        elif page == 'weekly_review':
            show_weekly_review()
        elif page == 'settings':
            show_settings()
        else:
            # Default home page
            show_daily_planning()


# ============================================================================
# RUN APP
# ============================================================================

if __name__ == "__main__":
    main()
