"""
ASGI config for foodcart project.
"""

import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'foodcart.settings')
application = get_asgi_application()
