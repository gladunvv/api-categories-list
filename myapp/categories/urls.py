from django.urls import path

from categories.views import CategoryView

app_name = 'categories'

urlpatterns = [
    path('<int:pk>', CategoryView.as_view(), name='category')
]