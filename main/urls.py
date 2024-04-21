from main import apps
from django.urls import path

from main.views import SendingListView

app_name = apps.MainConfig.name

urlpatterns = [
    path('', SendingListView.as_view(), name='sending_list'),
    # path('contacts/', ContactsTemplateView.as_view(), name='contacts'),
    # path('catalog/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name='product_detail'),
    # path('catalog/create/', ProductCreateView.as_view(), name='product_create'),
    # path('catalog/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    # path('catalog/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    # path('catalog/<int:pk>/moderate', ProductModerationView.as_view(), name='product_moderation'),
    # path('categories/', CategoryListView.as_view(), name='category_list'),
]