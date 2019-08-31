from django.urls import path

from categories.views import CategoryView, CategoryPostView

app_name = 'categories'

urlpatterns = [
    path('', CategoryPostView.as_view(), name='category_post'),
    path('<int:pk>', CategoryView.as_view(), name='category_get')
]