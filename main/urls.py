from main import apps
from django.urls import path
from django.views.decorators.cache import cache_page
from main.views import SendingListView, MessageListView, ClientListView, SendingDetailView, MessageDetailView, \
    ClientDetailView


app_name = apps.MainConfig.name

urlpatterns = [
    path('', SendingListView.as_view(), name='sending_list'),
    path('messages/', MessageListView.as_view(), name='message_list'),
    path('clients/', ClientListView.as_view(), name='client_list'),
    path('sending/<int:pk>/', cache_page(60)(SendingDetailView.as_view()), name='sending_detail'),
    path('message/<int:pk>/', cache_page(60)(MessageDetailView.as_view()), name='message_detail'),
    path('client/<int:pk>/', cache_page(60)(ClientDetailView.as_view()), name='client_detail'),
    # path('catalog/create/', ProductCreateView.as_view(), name='product_create'),
    # path('catalog/<int:pk>/update/', ProductUpdateView.as_view(), name='product_update'),
    # path('catalog/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    # path('catalog/<int:pk>/moderate', ProductModerationView.as_view(), name='product_moderation'),
]