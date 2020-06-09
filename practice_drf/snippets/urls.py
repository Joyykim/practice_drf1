from django.urls import path
from rest_framework.routers import SimpleRouter

from snippets.views import SnippetViewSet

router = SimpleRouter()
router.register(r'snippets', viewset=SnippetViewSet, basename='snippet')

urlpatterns = router.urls
