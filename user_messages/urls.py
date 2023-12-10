from django.urls import path

from .views import SendMessage, message_detail, list_messages, remove_message, SearchMessages


app_name = "user_messages"

urlpatterns = [
    path("received_messages/", list_messages, name="received_messages"),
    path("sent_messages/", list_messages, name="sent_messages"),
    path("archived_messages/", list_messages, name="archived_messages"),
    path("received_messages/<str:username>/<int:pk>", message_detail, name="received_message"),
    path("sent_messages/<str:username>/<int:pk>", message_detail, name="sent_message"),
    path("send_message/", SendMessage.as_view(), name="send_message"),
    path("remove_message/<str:msg_type>/<int:pk>", remove_message, name="remove_message"),
    path("search_messages/", SearchMessages.as_view(), name="search_messages"),
    path("search_messages/page/<int:page>", SearchMessages.as_view(), name="search_messages"),
]
