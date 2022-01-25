from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('favorite_food/<int:item_id>', views.favoriteFood),
    path('unfavorite_food/<int:item_id>', views.unfavoriteFood),
    path('register', views.register),
    path('register/create',views.createUser),
    path('login', views.login),
    path('logout', views.logout),
    path('item/<int:item_id>',views.item_data),
    path('new_item', views.new_item),
    path('new_item/create', views.new_item_create),
    path('edit_item/<int:item_id>',views.edit_item),
    path('edit_item/<int:item_id>/update',views.update_item),
    path('delete_item/<int:item_id>',views.delete_item)
]