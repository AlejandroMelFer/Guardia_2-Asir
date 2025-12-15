"""
WSGI config for kronoleon project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

# Add project root to sys.path to ensure custom apps are found
path = Path(__file__).resolve().parent.parent
if str(path) not in sys.path:
    sys.path.append(str(path))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kronoleon.settings')

application = get_wsgi_application()
