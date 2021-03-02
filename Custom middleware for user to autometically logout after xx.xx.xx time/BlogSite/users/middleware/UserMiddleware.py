from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib import auth
from django.utils.deprecation import MiddlewareMixin
from django.core.serializers.json import DjangoJSONEncoder
import json

class AutoLogout(MiddlewareMixin):

    def process_request(self, request):
        if not request.user.is_authenticated:
            return
        else:
            try:
                last_time = datetime.strptime(json.loads(
                    request.session['last_hit']), '%Y-%m-%d %H:%M:%S.%f')
                if (datetime.now() - last_time) > timedelta(0, settings.AUTO_LOGOUT_DELAY, 0):
                    auth.logout(request)
                    del request.session['last_hit']
                    request.session.modified = True
                    return
            except KeyError:
                pass
