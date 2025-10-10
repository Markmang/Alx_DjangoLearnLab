from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from .serializers import RegisterSerializer, UserSerializer
from notifications.utils import create_notification

CustomUser = get_user_model()


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user, token = serializer.save()
            return Response({
                "user": UserSerializer(user).data,
                "token": token
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        return Response({
            "token": token.key,
            "user": UserSerializer(user).data
        })


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# Follow user view
class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        current_user = request.user

        if target_user == current_user:
            return Response({"detail": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        current_user.following.add(target_user)
        create_notification(
            recipient=target_user,
            actor=current_user,
            verb="started following you",
            target=current_user
        )
        return Response({"detail": f"You are now following {target_user.username}."}, status=status.HTTP_200_OK)


# Unfollow user view
class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def post(self, request, user_id):
        target_user = get_object_or_404(CustomUser, id=user_id)
        current_user = request.user

        if target_user == current_user:
            return Response({"detail": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)

        current_user.following.remove(target_user)
        return Response({"detail": f"You have unfollowed {target_user.username}."}, status=status.HTTP_200_OK)
