from django.views.generic import ListView
from main.models import Sending
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
