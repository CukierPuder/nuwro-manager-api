from django.urls import path, include
from rest_framework.routers import DefaultRouter

from manager import views


router = DefaultRouter()
router.register('experiments', views.ExperimentViewSet)
router.register('measurements', views.MeasurementViewSet)
router.register('nuwroversions', views.NuwroversionViewSet)
router.register('artifacts', views.ArtifactViewSet)
router.register('resultfiles', views.ResultfileViewSet)

app_name = 'manager'

urlpatterns = [
    path('', include(router.urls))
]
