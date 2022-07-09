from cgitb import lookup
from django.urls import path
from . import views
from rest_framework_nested import routers

router=routers.DefaultRouter()
router.register('products',views.ProductViewSet,basename='products')
router.register('collections',views.CollectionViewSet)
router.register('carts',views.CartViewSet,basename='carts')
router.register('customers',views.CustomerViewSet)
router.register('orders',views.OrderViewSet)

product_routers=routers.NestedDefaultRouter(router,"products",lookup='product')
product_routers.register('reviews',views.ReviewViewSet,basename='product-reviews')

cart_routes=routers.NestedDefaultRouter(router,'carts',lookup='cart')
cart_routes.register('items',views.CartItemViewSet,basename='cart-items')


# URLConf
urlpatterns = router.urls+product_routers.urls+cart_routes.urls
