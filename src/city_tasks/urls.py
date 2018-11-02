from django.urls import path, include

from city_tasks_api.urls import router

urlpatterns = [
    path('', include(router.urls)),
]
