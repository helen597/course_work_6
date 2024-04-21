from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from main.models import Sending, Message, Client
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class SendingListView(LoginRequiredMixin, ListView):
    model = Sending
    template_name = 'main/sending_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'main/message_list.html'


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'main/client_list.html'


class SendingDetailView(DetailView):
    model = Sending
    template_name = ''
    
    
class MessageDetailView(DetailView):
    model = Message
    template_name = ''
    
    
class ClientDetailView(DetailView):
    model = Client
    template_name = ''
    