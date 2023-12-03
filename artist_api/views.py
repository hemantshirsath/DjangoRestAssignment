from django.shortcuts import render
from django.contrib import messages

import requests
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from rest_framework import generics, permissions, filters
from rest_framework.authtoken.models import Token
from .models import Artist, Work
from .serializers import ArtistSerializer, WorkSerializer, UserRegistrationSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework import generics, permissions, filters, status
from .forms import TokenObtainForm

class ObtainAuthTokenView(ObtainAuthToken):
    """Custom ObtainAuthToken view to return user details along with the token."""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk, 'username': user.username})
    
    def get(self, request, *args, **kwargs):
        # Implement your logic for handling GET requests here
        # For example, you might return information about the currently authenticated user
        user = request.user
        if user.is_authenticated:
            return Response({'user_id': user.pk, 'username': user.username})
        else:
            return Response({'detail': 'Not authenticated'}, status=401)

class OpenObtainAuthTokenView(ObtainAuthToken):
    """Custom ObtainAuthToken view to return user details along with the token."""

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk, 'username': user.username})


class OpenTokenInfoView(APIView):
    """View to get token information for an open endpoint."""

    def post(self, request, *args, **kwargs):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        if not username or not password:
            return Response({'detail': 'Both username and password are required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(password):
            return Response({'detail': 'Invalid credentials.'}, status=status.HTTP_400_BAD_REQUEST)

        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.pk, 'username': user.username})

class WorkListCreateView(generics.ListCreateAPIView):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['artists__name']

    def perform_create(self, serializer):
        serializer.save(artists=[self.request.user.artist])

class ArtistListCreateView(generics.ListCreateAPIView):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    permission_classes = [permissions.IsAuthenticated]

class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()

        # Create a token for the newly registered user
        token, created = Token.objects.get_or_create(user=user)

        # Return the token along with the registration response
        response_data = {
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            # Add other user details as needed
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    
@receiver(post_save, sender=User)
def create_artist_profile(sender, instance, created, **kwargs):
    if created:
        Artist.objects.create(user=instance)



def obtain_token(request):
    if request.method == 'POST':
        form = TokenObtainForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Make a POST request to the /api/token/ endpoint
            response = requests.post(
                'http://127.0.0.1:8000/api/token/',
                data={'username': username, 'password': password}
            )

            if response.status_code == 200:
                token_data = response.json()
                messages.success(request, f'Token obtained successfully for user {username}')
                return render(request, 'token_obtain_success.html', {'token_data': token_data})
            else:
                messages.error(request, 'Invalid credentials. Please try again.')
    else:
        form = TokenObtainForm()

    return render(request, 'token_obtain.html', {'form': form})