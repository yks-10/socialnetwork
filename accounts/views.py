from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.throttling import UserRateThrottle
from django.contrib.auth import get_user_model
from .models import Friendship
from .serializers import UserSerializer, FriendshipSerializer

User = get_user_model()


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get('email').lower()
        password = request.data.get('password')
        user = User.objects.filter(email=email).first()

        if user and user.check_password(password):
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]

    def get_queryset(self):
        query = self.request.query_params.get('q')
        if query:
            return User.objects.filter(
                Q(email__iexact=query) | Q(username__icontains=query)
            ).distinct()
        return User.objects.none()


class FriendRequestView(generics.CreateAPIView):
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        to_user_id = request.data.get('to_user_id')
        if Friendship.objects.filter(from_user=request.user, to_user_id=to_user_id, status='pending').exists():
            return Response({"message": "Friend request already sent"}, status=status.HTTP_400_BAD_REQUEST)

        friendship = Friendship.objects.create(from_user=request.user, to_user_id=to_user_id, status='pending')
        return Response(FriendshipSerializer(friendship).data, status=status.HTTP_201_CREATED)


class RespondFriendRequestView(views.APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        friendship_id = kwargs.get('id')
        action = request.data.get('action')

        try:
            friendship = Friendship.objects.get(id=friendship_id, to_user=request.user)
            if action == 'accept':
                friendship.status = 'accepted'
                friendship.save()
                return Response({"message": "Friend request accepted"}, status=status.HTTP_200_OK)
            elif action == 'reject':
                friendship.status = 'rejected'
                friendship.save()
                return Response({"message": "Friend request rejected"}, status=status.HTTP_200_OK)
        except Friendship.DoesNotExist:
            return Response({"message": "Invalid friend request"}, status=status.HTTP_400_BAD_REQUEST)


class ListFriendsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.friends.filter(friendship__status='accepted')


class ListPendingRequestsView(generics.ListAPIView):
    serializer_class = FriendshipSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.friendship_requests_received.filter(status='pending')
