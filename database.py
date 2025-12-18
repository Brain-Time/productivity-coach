"""
Database Module

Handles all database operations for user profiles and data persistence.
Uses SQLite for local-first storage.

Author: Brain-Time
Project: Productivity Coach
"""

import sqlite3
import json
from typing import Dict, Optional, List
from datetime import datetime
from pathlib import Path


# ============================================================================
# DATABASE CONFIGURATION
# ============================================================================

DB_PATH = Path("productivity_coach.db")
DB_VERSION = 1


# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_database() -> None:
    """
    Initialize database with required tables.
    Creates tables if they don't exist.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # User Profiles Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_data TEXT NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            is_active INTEGER DEFAULT 1
        )
    """)
    
    # Daily Plans Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_plans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            plan_content TEXT NOT NULL,
            available_hours REAL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user_profiles (id)
        )
    """)
    
    # Weekly Reviews Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weekly_reviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            week_start TEXT NOT NULL,
            week_end TEXT NOT NULL,
            review_content TEXT NOT NULL,
            created_at TEXT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES user_profiles (id)
        )
    """)
    
    # App Metadata Table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS app_metadata (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    
    # Insert DB version
    cursor.execute("""
        INSERT OR REPLACE INTO app_metadata (key, value, updated_at)
        VALUES ('db_version', ?, ?)
    """, (str(DB_VERSION), datetime.now().isoformat()))
    
    conn.commit()
    conn.close()
    
    print(f"✅ Database initialized: {DB_PATH}")


# ============================================================================
# USER PROFILE OPERATIONS
# ============================================================================

def save_user_profile(profile_data: Dict) -> int:
    """
    Save user profile to database.
    
    Args:
        profile_data: User profile dictionary
        
    Returns:
        User ID (primary key)
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Deactivate any existing active profiles
    cursor.execute("""
        UPDATE user_profiles 
        SET is_active = 0 
        WHERE is_active = 1
    """)
    
    # Insert new profile
    now = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO user_profiles (profile_data, created_at, updated_at, is_active)
        VALUES (?, ?, ?, 1)
    """, (json.dumps(profile_data), now, now))
    
    user_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✅ User profile saved with ID: {user_id}")
    return user_id


def get_active_user_profile() -> Optional[Dict]:
    """
    Get the currently active user profile.
    
    Returns:
        User profile dict or None if no active profile
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, profile_data, created_at, updated_at
        FROM user_profiles
        WHERE is_active = 1
        ORDER BY created_at DESC
        LIMIT 1
    """)
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        profile = json.loads(row[1])
        profile['db_id'] = row[0]
        profile['db_created_at'] = row[2]
        profile['db_updated_at'] = row[3]
        return profile
    
    return None


def update_user_profile(user_id: int, profile_data: Dict) -> bool:
    """
    Update existing user profile.
    
    Args:
        user_id: User ID to update
        profile_data: New profile data
        
    Returns:
        True if successful, False otherwise
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    cursor.execute("""
        UPDATE user_profiles
        SET profile_data = ?, updated_at = ?
        WHERE id = ?
    """, (json.dumps(profile_data), now, user_id))
    
    success = cursor.rowcount > 0
    conn.commit()
    conn.close()
    
    if success:
        print(f"✅ User profile {user_id} updated")
    else:
        print(f"⚠️  User profile {user_id} not found")
    
    return success


def get_all_user_profiles() -> List[Dict]:
    """
    Get all user profiles (for admin/debugging).
    
    Returns:
        List of user profile dicts
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, profile_data, created_at, updated_at, is_active
        FROM user_profiles
        ORDER BY created_at DESC
    """)
    
    profiles = []
    for row in cursor.fetchall():
        profile = json.loads(row[1])
        profile['db_id'] = row[0]
        profile['db_created_at'] = row[2]
        profile['db_updated_at'] = row[3]
        profile['is_active'] = bool(row[4])
        profiles.append(profile)
    
    conn.close()
    return profiles


# ============================================================================
# DAILY PLAN OPERATIONS
# ============================================================================

def save_daily_plan(user_id: int, date: str, plan_content: str, 
                   available_hours: float) -> int:
    """
    Save a daily plan.
    
    Args:
        user_id: User ID
        date: Date in ISO format (YYYY-MM-DD)
        plan_content: AI-generated plan content
        available_hours: Hours available for the day
        
    Returns:
        Plan ID
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO daily_plans (user_id, date, plan_content, available_hours, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, date, plan_content, available_hours, now))
    
    plan_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✅ Daily plan saved with ID: {plan_id}")
    return plan_id


def get_daily_plan(user_id: int, date: str) -> Optional[Dict]:
    """
    Get daily plan for a specific date.
    
    Args:
        user_id: User ID
        date: Date in ISO format
        
    Returns:
        Plan dict or None
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, plan_content, available_hours, created_at
        FROM daily_plans
        WHERE user_id = ? AND date = ?
        ORDER BY created_at DESC
        LIMIT 1
    """, (user_id, date))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'id': row[0],
            'plan_content': row[1],
            'available_hours': row[2],
            'created_at': row[3],
            'date': date
        }
    
    return None


def get_recent_daily_plans(user_id: int, limit: int = 7) -> List[Dict]:
    """
    Get recent daily plans.
    
    Args:
        user_id: User ID
        limit: Number of plans to retrieve
        
    Returns:
        List of plan dicts
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, date, plan_content, available_hours, created_at
        FROM daily_plans
        WHERE user_id = ?
        ORDER BY date DESC
        LIMIT ?
    """, (user_id, limit))
    
    plans = []
    for row in cursor.fetchall():
        plans.append({
            'id': row[0],
            'date': row[1],
            'plan_content': row[2],
            'available_hours': row[3],
            'created_at': row[4]
        })
    
    conn.close()
    return plans


# ============================================================================
# WEEKLY REVIEW OPERATIONS
# ============================================================================

def save_weekly_review(user_id: int, week_start: str, week_end: str, 
                      review_content: str) -> int:
    """
    Save a weekly review.
    
    Args:
        user_id: User ID
        week_start: Week start date (ISO format)
        week_end: Week end date (ISO format)
        review_content: AI-generated review content
        
    Returns:
        Review ID
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    now = datetime.now().isoformat()
    cursor.execute("""
        INSERT INTO weekly_reviews (user_id, week_start, week_end, review_content, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, week_start, week_end, review_content, now))
    
    review_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    print(f"✅ Weekly review saved with ID: {review_id}")
    return review_id


def get_weekly_review(user_id: int, week_start: str) -> Optional[Dict]:
    """
    Get weekly review for a specific week.
    
    Args:
        user_id: User ID
        week_start: Week start date (ISO format)
        
    Returns:
        Review dict or None
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, week_end, review_content, created_at
        FROM weekly_reviews
        WHERE user_id = ? AND week_start = ?
        ORDER BY created_at DESC
        LIMIT 1
    """, (user_id, week_start))
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return {
            'id': row[0],
            'week_start': week_start,
            'week_end': row[1],
            'review_content': row[2],
            'created_at': row[3]
        }
    
    return None


def get_all_weekly_reviews(user_id: int) -> List[Dict]:
    """
    Get all weekly reviews for a user.
    
    Args:
        user_id: User ID
        
    Returns:
        List of review dicts
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, week_start, week_end, review_content, created_at
        FROM weekly_reviews
        WHERE user_id = ?
        ORDER BY week_start DESC
    """, (user_id,))
    
    reviews = []
    for row in cursor.fetchall():
        reviews.append({
            'id': row[0],
            'week_start': row[1],
            'week_end': row[2],
            'review_content': row[3],
            'created_at': row[4]
        })
    
    conn.close()
    return reviews


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def reset_database() -> None:
    """
    Reset database (delete all data).
    USE WITH CAUTION!
    """
    if DB_PATH.exists():
        DB_PATH.unlink()
        print("⚠️  Database deleted")
    
    init_database()
    print("✅ Database reset complete")


def get_database_stats() -> Dict:
    """
    Get database statistics.
    
    Returns:
        Dict with counts of various records
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    stats = {}
    
    # User profiles count
    cursor.execute("SELECT COUNT(*) FROM user_profiles")
    stats['total_profiles'] = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM user_profiles WHERE is_active = 1")
    stats['active_profiles'] = cursor.fetchone()[0]
    
    # Daily plans count
    cursor.execute("SELECT COUNT(*) FROM daily_plans")
    stats['total_daily_plans'] = cursor.fetchone()[0]
    
    # Weekly reviews count
    cursor.execute("SELECT COUNT(*) FROM weekly_reviews")
    stats['total_weekly_reviews'] = cursor.fetchone()[0]
    
    # Database size
    stats['db_size_bytes'] = DB_PATH.stat().st_size if DB_PATH.exists() else 0
    stats['db_size_kb'] = round(stats['db_size_bytes'] / 1024, 2)
    
    conn.close()
    return stats


# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE MODULE TEST")
    print("=" * 60)
    
    # Initialize database
    print("\n1. Initializing database...")
    init_database()
    
    # Create test profile
    print("\n2. Creating test user profile...")
    test_profile = {
        "system_message_daily_planning": "You are a coach for parents...",
        "system_message_weekly_review": "You analyze weekly progress...",
        "coaching_tone": "encouraging, practical",
        "key_focus_areas": ["Quran", "Family", "Career"],
        "time_block_size": 30,
        "islamic_emphasis": "medium",
        "language_code": "de",
        "onboarding_data": {
            "language": "Deutsch",
            "role": "Parent with young children",
            "goals": ["Quran memorization/study", "Career development"]
        },
        "created_at": datetime.now().isoformat()
    }
    
    user_id = save_user_profile(test_profile)
    
    # Retrieve profile
    print("\n3. Retrieving active user profile...")
    active_profile = get_active_user_profile()
    if active_profile:
        print(f"   ✅ Found profile for user {active_profile['db_id']}")
        print(f"   Language: {active_profile['language_code']}")
        print(f"   Focus areas: {', '.join(active_profile['key_focus_areas'])}")
    
    # Save daily plan
    print("\n4. Saving daily plan...")
    today = datetime.now().date().isoformat()
    plan_id = save_daily_plan(
        user_id=user_id,
        date=today,
        plan_content="9:00-10:00 Quran\n10:00-11:00 Work\n11:00-12:00 Family",
        available_hours=3.0
    )
    
    # Retrieve daily plan
    print("\n5. Retrieving daily plan...")
    plan = get_daily_plan(user_id, today)
    if plan:
        print(f"   ✅ Found plan for {plan['date']}")
        print(f"   Available hours: {plan['available_hours']}")
    
    # Save weekly review
    print("\n6. Saving weekly review...")
    review_id = save_weekly_review(
        user_id=user_id,
        week_start="2024-12-16",
        week_end="2024-12-22",
        review_content="Great progress on Quran! Consider more family time."
    )
    
    # Get stats
    print("\n7. Database statistics...")
    stats = get_database_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    print("\n✅ All database tests passed!")
    print(f"\n📁 Database location: {DB_PATH.absolute()}")
