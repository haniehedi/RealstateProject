
from rest_framework import routers
from . import views
app_name = 'listing'
router = routers.DefaultRouter()
router.register('properties', views.PropertyViewSet, basename='properties')
router.register('agents', views.AgentViewSet, basename='agents')
urlpatterns = router.urls
