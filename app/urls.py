from django.urls import path
from .views import start, kill, home, analytics
app_name = 'app'
urlpatterns = [
    path('', home, name='home'),
    path('start', start, name='start'),
    path('kill', kill, name='kill'),
    path('analytics', analytics, name='analytics'),
]
