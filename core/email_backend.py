# ========================================
# CUSTOM EMAIL BACKEND - For SSL Issues
# ========================================
# Create this file: backend/core/email_backend.py

import ssl
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend


class CustomEmailBackend(SMTPBackend):
    """
    Custom email backend that bypasses SSL certificate verification.
    WARNING: Only use for development/testing on macOS with Python 3.13
    DO NOT use in production!
    """
    
    @property
    def ssl_context(self):
        """Return an unverified SSL context."""
        if self.ssl_certfile or self.ssl_keyfile:
            ssl_context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_CLIENT)
            ssl_context.load_cert_chain(self.ssl_certfile, self.ssl_keyfile)
            return ssl_context
        else:
            # Return unverified context to bypass certificate verification
            return ssl._create_unverified_context()