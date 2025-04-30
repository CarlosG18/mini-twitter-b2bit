from rest_framework import routers
from .views import UserViewSet, PostViewSet

router = routers.DefaultRouter()

# registrando as rotas das views
router.register(r'users', UserViewSet)
router.register(r'posts', PostViewSet)

urlpatterns = router.urls