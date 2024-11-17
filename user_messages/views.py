from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import FormView, ListView
from django.db.models import Q

from jalali_date import datetime2jalali
from utils.tools import messages_filters, messages_pagination, get_all_logged_in_users
from account.models import User
from account.models import UserActionsLog
from .models import Message
from .forms import MessageForm



class SendMessage(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, FormView):
    permission_required = 'user_messages.write_message'
    template_name = "user_messages/send_message.html"
    form_class = MessageForm
    success_url = reverse_lazy('user_messages:sent_messages')
    success_message = "پیام شما با موفقیت ارسال گردید"

    def form_valid(self, form):
        receiver_username = self.request.GET.get('receiver')
        if receiver_username is not None:
            receiver = get_object_or_404(User, username=receiver_username)
        else:
            receiver_obj = form.cleaned_data.get('receiver_name')
            receiver = get_object_or_404(User, pk=receiver_obj.id) # type: ignore
        subject = form.cleaned_data.get('subject')
        content = form.cleaned_data.get('content')
        if receiver == self.request.user:
            form.add_error('receiver_name', 'گیرنده پیام باید کاربری غیر از شما باشد')
            return super().form_invalid(form)
        else:
            Message.objects.create(sender=self.request.user, receiver=receiver, 
            subject=subject, content=content, seen=False)
            UserActionsLog.objects.create(user=self.request.user, log_type="CR", log_content=f"ارسال پیام به «{receiver.get_full_name()}»")
            return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["received_count"] = messages_filters(self.request)['received_count']
        context["sent_count"] = messages_filters(self.request)['sent_count']
        context["unseen_count"] = messages_filters(self.request)['unseen_count']
        context["archived_count"] = messages_filters(self.request)['archived_count']
        return context


class SearchMessages(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'user_messages.seen_message'
    template_name = "user_messages/search_messages.html"
    model = Message
    context_object_name = "found_messages"
    paginate_by = 10

    def get_queryset(self):
        global query
        query = self.request.GET.get('data_search')

        global search_result
        search_result = Message.objects.search(query).filter( # type: ignore
            Q(receiver=self.request.user, visible_receiver=True) |
            Q(sender=self.request.user, visible_sender=True)
        )
        
        return search_result
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = query
        context["received_count"] = messages_filters(self.request)['received_count']
        context["sent_count"] = messages_filters(self.request)['sent_count']
        context["unseen_count"] = messages_filters(self.request)['unseen_count']
        context["archived_count"] = messages_filters(self.request)['archived_count']
        return context
    

@login_required
@permission_required('user_messages.seen_message')
def list_messages(request):
    if request.method == 'POST' and request.resolver_match.url_name == 'received_messages':
        msg_id = request.POST.get('arc_receive_id')
        msg_obj = get_object_or_404(Message, pk=int(msg_id))
        msg_obj.archive_receiver = True
        msg_obj.save()
    elif request.method == 'POST' and request.resolver_match.url_name == 'sent_messages':
        msg_id = request.POST.get('arc_sent_id')
        msg_obj = get_object_or_404(Message, pk=int(msg_id))
        msg_obj.archive_sender = True
        msg_obj.save()
    elif request.method == 'POST' and request.resolver_match.url_name == 'archived_messages':
        receive_id = request.POST.get('rec_receive_id')
        sent_id = request.POST.get('rec_sent_id')
        if receive_id:
            receive_obj = get_object_or_404(Message, pk=int(receive_id))
            receive_obj.archive_receiver = False
            receive_obj.save()
        else:
            sent_obj = get_object_or_404(Message, pk=int(sent_id))
            sent_obj.archive_sender = False
            sent_obj.save()

    context = {
        'page_obj': messages_pagination(request),
        'received_count': messages_filters(request)['received_count'],
        'sent_count': messages_filters(request)['sent_count'],
        'unseen_count': messages_filters(request)['unseen_count'],
        'archived_count': messages_filters(request)['archived_count']
    }

    return render(request, "user_messages/list_messages.html", context)


@login_required
@permission_required('user_messages.seen_message')
def remove_message(request, **kwargs):
    msg_type = kwargs['msg_type']
    pk = kwargs['pk']
    msg = get_object_or_404(Message, pk=pk)
    request_path = request.get_full_path().split('/')[2]
    if not msg_type in ['received', 'sent', 'ar_received', 'ar_sent']:
        raise Http404()
    elif msg_type == 'received' or msg_type == 'ar_received':
        UserActionsLog.objects.create(user=request.user, log_type="DL", log_content=f"حذف پیام دریافتی از «{msg.sender.get_full_name()}»")
        msg.visible_receiver = False
        msg.save()
    else:
        UserActionsLog.objects.create(user=request.user, log_type="DL", log_content=f"حذف پیام ارسالی به «{msg.receiver.get_full_name()}»")
        msg.visible_sender = False
        msg.save()

    if not msg.visible_receiver and not msg.visible_sender:
        msg.delete()

    if msg_type == 'ar_received' or msg_type == 'ar_sent':
        return redirect('user_messages:archived_messages')
    elif msg_type == 'received':
        return redirect('user_messages:received_messages')
    else:
        return redirect('user_messages:sent_messages')


@login_required
@permission_required('user_messages.seen_message')
def message_detail(request, **kwargs):
    username = kwargs['username'] # sender in received messages & receiver in sent messages
    pk = kwargs['pk']
    msg = get_object_or_404(Message, pk=pk)
    
    if request.resolver_match.url_name == 'received_message':
        # check sender for received messages
        if msg.sender.username != username:
            raise Http404()
        # check receiver for received messages
        elif msg.receiver.username != request.user.username:
            raise Http404()

        if not msg.seen:
            msg.seen = True
            msg.save()

    elif request.resolver_match.url_name == 'sent_message':
        # check sender for sent messages
        if msg.sender.username != request.user.username:
            raise Http404()
        # check receiver for sent messages
        elif msg.receiver.username != username:
            raise Http404()

    context = {
        'msg': msg,
        'j_date_time': datetime2jalali(msg.date_time).strftime('%Y/%m/%d _ %H:%M:%S'), # type: ignore
        'received_count': messages_filters(request)['received_count'],
        'sent_count': messages_filters(request)['sent_count'],
        'unseen_count': messages_filters(request)['unseen_count'],
        'archived_count': messages_filters(request)['archived_count'],
    }

    return render(request, "user_messages/message_detail.html", context)
