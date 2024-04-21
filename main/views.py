from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from main.forms import SendingForm, MessageForm, ClientForm
from main.models import Sending, Message, Client
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


# Create your views here.
class SendingListView(LoginRequiredMixin, ListView):
    model = Sending
    template_name = 'main/sending_list.html'

    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        # if not self.request.user.is_staff:
        #     queryset = queryset.filter(owner=self.request.user)
        return queryset


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = 'main/message_list.html'


class ClientListView(LoginRequiredMixin, ListView):
    model = Client
    template_name = 'main/client_list.html'


class SendingDetailView(DetailView):
    model = Sending
    template_name = 'main/sending_detail.html'
    
    
class MessageDetailView(DetailView):
    model = Message
    template_name = 'main/message_detail.html'
    
    
class ClientDetailView(DetailView):
    model = Client
    template_name = 'main/client_detail.html'


class SendingCreateView(LoginRequiredMixin, CreateView):
    model = Sending
    form_class = SendingForm
    success_url = reverse_lazy('main:sending_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()
        return super().form_valid(form)


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:message_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"

    # def form_valid(self, form):
    #     self.object = form.save()
    #     self.object.owner = self.request.user
    #     self.object.save()
    #     return super().form_valid(form)


class ClientCreateView(LoginRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:client_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"

    # def form_valid(self, form):
    #     self.object = form.save()
    #     self.object.owner = self.request.user
    #     self.object.save()
    #     return super().form_valid(form)


class SendingUpdateView(LoginRequiredMixin, UpdateView):
    model = Sending
    form_class = SendingForm
    success_url = reverse_lazy('main:sending_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner == self.request.user or self.request.user.has_perm('catalog.change_product'):
            return self.object
        raise PermissionDenied

    # def get_context_data(self, **kwargs):
    #     context_data = super().get_context_data(**kwargs)
    #     VersionFormset = inlineformset_factory(Product, Version, form=VersionForm, extra=1)
    #     if self.request.method == 'POST':
    #         context_data['formset'] = VersionFormset(self.request.POST, instance=self.object)
    #     else:
    #         context_data['formset'] = VersionFormset(instance=self.object)
    #     return context_data

    def form_valid(self, form):
        context_data = self.get_context_data()
        formset = context_data['formset']
        if form.is_valid() and formset.is_valid():
            self.object = form.save()
            formset.instance=self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form, formset=formset))


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    form_class = MessageForm
    success_url = reverse_lazy('main:message_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    success_url = reverse_lazy('main:client_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"


class SendingDeleteView(LoginRequiredMixin, DeleteView):
    model = Sending
    success_url = reverse_lazy('main:sending_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('main:message_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    model = Client
    success_url = reverse_lazy('main:client_list')
    login_url = reverse_lazy('users:login')
    redirect_field_name = "redirect_to"
