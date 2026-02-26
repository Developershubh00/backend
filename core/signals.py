# core/signals.py
"""
Django Signals for BLC Core App.
Fires after a new user is successfully created and saved to the database.
Signal is decoupled from signup view — works regardless of where signup happens.
"""

import logging
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model

from .google_sheets import append_signup_to_sheet

logger = logging.getLogger(__name__)

User = get_user_model()


@receiver(post_save, sender=User)
def sync_new_signup_to_google_sheets(sender, instance, created, **kwargs):
    """
    Fires ONLY when a brand new user is created (created=True).
    Does NOT fire on profile updates, password changes, OTP saves, etc.
    
    Flow:
      User hits signup API
        → serializer.save() → user.save() → DB write ✅
          → post_save signal fires (created=True)
            → append_signup_to_sheet(user) 
              → Google Sheet updated ✅
              → JWT token returned to frontend ✅ (sheet sync does not block this)
    """
    if not created:
        # This is an update (profile edit, password reset, OTP save, etc.)
        # Do nothing — we only want NEW signups
        return

    logger.info(
        "New user created: %s (ID: %s) — syncing to Google Sheets...",
        instance.email, instance.id
    )

    # Push to Google Sheets (errors are caught inside, will not crash signup)
    append_signup_to_sheet(instance)