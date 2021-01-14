----------------
In settings.py : 
----------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR,"reactapp/build"),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'reactapp/build/static')
]



-----------------
in urls.py:
-----------------
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),\
    path('',TemplateView.as_view(template_name = "index.html"))
]


--------
cmd:
--------

1. install npm
2. npx create-react-app <name>
3. npm run build


