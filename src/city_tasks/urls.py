from django.urls import path, include
from rest_framework_swagger.views import get_swagger_view

from city_tasks_api.urls import router


schema_view = get_swagger_view(title='City tasks API')


urlpatterns = [
    path('', include(router.urls)),
    path('api_doc/', schema_view)
]
