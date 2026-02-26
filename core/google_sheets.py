# # core/google_sheets.py
# """
# Google Sheets Service for BLC Leads Tracking.
# Handles real-time sync of signup data to Google Sheets.
# This file is standalone - does not touch any existing code.
# """

# import logging
# from datetime import datetime
# from django.conf import settings

# logger = logging.getLogger(__name__)


# def get_sheets_client():
#     """
#     Returns an authenticated gspread client using service account credentials.
#     Returns None if credentials are not configured (safe fallback).
#     """
#     try:
#         import gspread
#         from google.oauth2.service_account import Credentials

#         scopes = [
#             'https://www.googleapis.com/auth/spreadsheets',
#             'https://www.googleapis.com/auth/drive',
#         ]

#         creds = Credentials.from_service_account_file(
#             settings.GOOGLE_SHEETS_CREDENTIALS_FILE,
#             scopes=scopes
#         )
#         client = gspread.authorize(creds)
#         return client

#     except FileNotFoundError:
#         logger.error(
#             "Google Sheets credentials file not found at: %s",
#             settings.GOOGLE_SHEETS_CREDENTIALS_FILE
#         )
#         return None
#     except Exception as e:
#         logger.error("Failed to initialize Google Sheets client: %s", str(e))
#         return None


# def append_signup_to_sheet(user):
#     """
#     Appends a new signup row to the Google Sheet.
    
#     Called from the Django signal after user.save() completes.
#     If anything fails here, it LOGS the error but does NOT crash signup.
    
#     Row format:
#     [Timestamp, Full Name, Email, Phone, NEET Rank, Category, State, User ID]
#     """
#     try:
#         client = get_sheets_client()
#         if client is None:
#             logger.warning(
#                 "Skipping Google Sheets sync — client not available. User: %s",
#                 user.email
#             )
#             return

#         sheet_id = settings.GOOGLE_SHEETS_SIGNUP_SHEET_ID
#         worksheet_name = getattr(
#             settings, 'GOOGLE_SHEETS_SIGNUP_WORKSHEET_NAME', 'Sheet1'
#         )

#         # Open the spreadsheet and worksheet
#         spreadsheet = client.open_by_key(sheet_id)
#         worksheet = spreadsheet.worksheet(worksheet_name)

#         # Build the row data — matches your column headers exactly
#         full_name = user.first_name or user.username or 'N/A'
#         timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

#         row = [
#             timestamp,                                  # Column A: Timestamp
#             full_name,                                  # Column B: Full Name
#             user.email or 'N/A',                        # Column C: Email
#             getattr(user, 'phone', '') or 'N/A',        # Column D: Phone
#             getattr(user, 'neet_rank', '') or 'N/A',    # Column E: NEET Rank
#             getattr(user, 'category', '') or 'N/A',     # Column F: Category
#             getattr(user, 'state', '') or 'N/A',        # Column G: State
#             str(user.id),                               # Column H: User ID
#         ]

#         # Append the row to the next empty row in the sheet
#         worksheet.append_row(row, value_input_option='USER_ENTERED')

#         logger.info(
#             "✅ Google Sheets: New signup synced — %s (User ID: %s)",
#             user.email, user.id
#         )

#     except Exception as e:
#         # CRITICAL: We only log, never raise.
#         # Signup flow must never fail because of Google Sheets.
#         logger.error(
#             "❌ Google Sheets sync failed for user %s: %s",
#             getattr(user, 'email', 'unknown'), str(e)
#         )

# core/google_sheets.py
"""
Google Sheets Service for BLC Leads Tracking.
Handles real-time sync of signup data to Google Sheets.
"""

import logging
from datetime import datetime
from django.conf import settings

logger = logging.getLogger(__name__)


# def get_sheets_client():
#     """
#     Returns an authenticated gspread client using service account credentials.
#     Returns None if credentials are not configured (safe fallback).
#     """
#     try:
#         import gspread
#         from google.oauth2.service_account import Credentials

#         scopes = [
#             'https://www.googleapis.com/auth/spreadsheets',
#             'https://www.googleapis.com/auth/drive',
#         ]

#         creds = Credentials.from_service_account_file(
#             settings.GOOGLE_SHEETS_CREDENTIALS_FILE,
#             scopes=scopes
#         )
#         client = gspread.authorize(creds)
#         return client

#     except FileNotFoundError:
#         logger.error(
#             "Google Sheets credentials file not found at: %s",
#             settings.GOOGLE_SHEETS_CREDENTIALS_FILE
#         )
#         return None
#     except Exception as e:
#         logger.error("Failed to initialize Google Sheets client: %s", str(e))
#         return None

def get_sheets_client():
    try:
        import gspread
        import json
        from google.oauth2.service_account import Credentials
        from django.conf import settings

        scopes = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive',
        ]

        # ── Try env variable first (Render production) ──
        creds_json = getattr(settings, 'GOOGLE_SHEETS_CREDENTIALS_JSON', '')
        if creds_json:
            creds_dict = json.loads(creds_json)
            creds = Credentials.from_service_account_info(creds_dict, scopes=scopes)
        else:
            # ── Fall back to file (local development) ───
            creds = Credentials.from_service_account_file(
                settings.GOOGLE_SHEETS_CREDENTIALS_FILE,
                scopes=scopes
            )

        return gspread.authorize(creds)

    except Exception as e:
        logger.error("Failed to initialize Google Sheets client: %s", str(e))
        return None

def _get_sheet():
    """Returns the gspread worksheet object."""
    client = get_sheets_client()
    if client is None:
        raise Exception("Google Sheets client not available")

    sheet_id = settings.GOOGLE_SHEETS_SIGNUP_SHEET_ID
    worksheet_name = getattr(
        settings, 'GOOGLE_SHEETS_SIGNUP_WORKSHEET_NAME', 'Sheet1'
    )
    spreadsheet = client.open_by_key(sheet_id)
    return spreadsheet.worksheet(worksheet_name)


def _classify_source(user) -> str:
    """
    Returns a human label for each signup's traffic source.
    Used by Hritik to filter paid vs organic leads instantly.
    """
    medium   = (getattr(user, 'utm_medium', '') or '').lower()
    source   = (getattr(user, 'utm_source', '') or '').lower()
    gclid    =  getattr(user, 'gclid', '')    or ''
    referrer = (getattr(user, 'referrer', '') or '').lower()

    if gclid or medium in ('cpc', 'ppc', 'paid', 'paid_search'):
        if any(s in source for s in ['facebook', 'instagram', 'meta']):
            return 'Meta Ads'
        return 'Google Ads'

    if medium == 'organic' or (not medium and any(
        s in referrer for s in ['google.', 'bing.', 'yahoo.'])):
        return 'Organic Search'

    if medium == 'social' or any(
        s in source for s in ['facebook', 'instagram', 'twitter', 'linkedin', 'youtube']):
        return 'Social'

    if medium == 'email':
        return 'Email'

    if referrer and 'believersconsultancy' not in referrer:
        return 'Referral'

    return 'Direct'


def append_signup_to_sheet(user) -> None:
    """
    Appends a new signup row to the Google Sheet.

    Called from the Django signal after user.save() completes.
    If anything fails here, it LOGS the error but does NOT crash signup.

    Sheet columns (in order):
    Timestamp | Full Name | Email | Phone | NEET Rank | Category | State | User ID
    utm_source | utm_medium | utm_campaign | utm_term | utm_content | gclid
    Referrer | Landing URL | IP Address | Source Type
    """
    try:
        sheet = _get_sheet()
        source_type = _classify_source(user)

        full_name = user.first_name or user.username or 'N/A'

        row = [
            datetime.now().strftime('%Y-%m-%d %H:%M:%S'),  # Timestamp
            full_name,                                      # Full Name
            user.email or 'N/A',                           # Email
            getattr(user, 'phone', '')      or '',          # Phone
            getattr(user, 'neet_rank', '')  or 'N/A',      # NEET Rank
            getattr(user, 'category', '')   or 'N/A',      # Category
            getattr(user, 'state', '')      or 'N/A',      # State
            str(user.id),                                   # User ID
            # ── UTM columns ──────────────────────────────
            getattr(user, 'utm_source', '')   or '',        # utm_source
            getattr(user, 'utm_medium', '')   or '',        # utm_medium
            getattr(user, 'utm_campaign', '') or '',        # utm_campaign
            getattr(user, 'utm_term', '')     or '',        # utm_term
            getattr(user, 'utm_content', '')  or '',        # utm_content
            getattr(user, 'gclid', '')        or '',        # gclid
            getattr(user, 'referrer', '')     or '',        # Referrer
            getattr(user, 'landing_url', '')  or '',        # Landing URL
            str(getattr(user, 'signup_ip', '') or ''),      # IP Address
            # ── Derived label ─────────────────────────────
            source_type,   # Google Ads / Meta Ads / Organic Search / Social / Referral / Direct
        ]

        sheet.append_row(row, value_input_option='USER_ENTERED')

        logger.info(
            "✅ Google Sheets: signup synced — %s (User ID: %s) — Source: %s",
            user.email, user.id, source_type
        )

    except Exception as exc:
        # CRITICAL: Only log, never raise — signup must never fail because of Sheets
        logger.error(
            "❌ Google Sheets sync failed for user %s: %s",
            getattr(user, 'email', 'unknown'), str(exc)
        )