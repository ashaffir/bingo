import platform
# from forex_python.converter import CurrencyRates # https://github.com/MicroPyramid/forex-python
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Q

def debug_mode(request):
    context = {}
    context['debug'] = settings.DEBUG        
    return context
