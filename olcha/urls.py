
from django.urls import path,include
from olcha import views
from rest_framework.routers import DefaultRouter
from olcha import auth
router = DefaultRouter()
router.register('categories', views.CategoryModelViewSet,basename = 'category')
router.register('products',views.ProductModelViewSet,basename='product')


urlpatterns = [
    # 1 st and 2nd version Barcha malumotlarni bitta viewda ciqarish uchun
    path('category-list/',views.CategoryListView.as_view(), name = 'category_list'),
    path('products/',views.ProductListView.as_view(),name = 'products'),
    path('comments/',views.CommentListView.as_view(),name = 'comments'),
    # path('users/',views.UserListView.as_view(), name = 'users'),
    # path('register/',views.register.as_view(), name = 'register'),
    path('category-list-generic-api-view/',views.CategoryList.as_view(),name = 'category-list'),
    path('category-detail-generic-api-view/<int:pk>/',views.CategoryDetail.as_view(),name = 'category-list'),
    path('category-add-generic-api-view/',views.CategoryAdd.as_view(),name = 'category-add'),
    path('category-delete-generic-api-view/<int:pk>/',views.CategoryDelete.as_view(),name = 'category-delete'),
    path('category-list-create-generic-api-view/',views.CategoryListCreate.as_view(),name = 'category-list-create'),
    path('category-update-generic-api-view/<int:pk>/',views.CategoryChange.as_view(),name = 'category-update'),
    path('modelviewset/',include(router.urls)),
    # for product section

    path('product-list-generic-api-view/',views.ProductList.as_view(),name = 'product-list'),
    # path('product-detail-generic-api-view/<int:pk>/',views.ProductDetail.as_view(),name = 'product-list'),
    path('product-add-generic-api-view/',views.ProductAdd.as_view(),name = 'product-add'),
    path('product-delete-generic-api-view/<int:pk>/',views.ProductDelete.as_view(),name = 'product-delete'),
    path('product-list-create-generic-api-view/',views.ProductListCreate.as_view(),name = 'product-list-create'),
    path('product-update-generic-api-view/<int:pk>/',views.ProductChange.as_view(),name = 'product-update'),
    path('modelviewset/',include(router.urls)),


    # Login Register Logout

    path("login/", auth.UserLoginAPIView.as_view(), name="user_login"),
    path("register/", auth.UserRegisterAPIView().as_view(), name="user_register"),
    path("logout/", auth.UserLogoutAPIView.as_view(), name="user_logout")
    

  
]
