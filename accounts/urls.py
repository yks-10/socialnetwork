from django.urls import path
from .views import SignupView, LoginView, UserSearchView, FriendRequestView, RespondFriendRequestView, ListFriendsView, ListPendingRequestsView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
    path('search/', UserSearchView.as_view(), name='search'),
    path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
    path('respond-request/<int:id>/', RespondFriendRequestView.as_view(), name='respond-request'),
    path('friends/', ListFriendsView.as_view(), name='friends'),
    path('pending-requests/', ListPendingRequestsView.as_view(), name='pending-requests'),
]
