"""
ASGI config for swiggy_clone project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'swiggy_clone.settings')
application = get_asgi_application()
