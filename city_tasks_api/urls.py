from .routers import CustomRouter
from .views import ClientsViewSet, TasksViewSet

router = CustomRouter()
router.register(r'a/v1/clients', ClientsViewSet, base_name='client')
router.register(r'a/v1/tasks', TasksViewSet, base_name='tasks')
