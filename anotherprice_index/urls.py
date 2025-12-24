from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('member_login/', views.member_login_view, name='member_login'),
    path('book_detail/<int:id>', views.book_detail_view, name='book_detail'),
    path('checkout_page/', views.checkout_page_view, name='checkout_page'),
    path('member_centre/', views.member_centre_view, name='member_centre'),
    path('member_email/', views.member_email_view, name='member_email'),
    path('member_point/', views.member_point_view, name='member_point'),
    path('member_profile/', views.member_profile_view, name='member_profile'),
    path('member_register/', views.member_register_view, name='member_register'),
    path('search_results/', views.search_results_view, name='search_results'),
    path('shopping_cart/', views.shopping_cart_view, name='shopping_cart'),
    path('logout/', views.logout_view, name='logout'),
]