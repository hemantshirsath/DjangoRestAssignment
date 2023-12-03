# from django.shortcuts import render
# from django.urls import reverse_lazy
# from rest_framework import generics, viewsets, permissions, filters
# from rest_framework.response import Response
# from rest_framework import status
# from .models import Artist, Work
# from .serializers import ArtistSerializer, WorkSerializer, WorkTypeSerializer, ArtistDetailSerializer
# from .forms import ArtistRegistrationForm, WorkForm
# from rest_framework.authtoken.models import Token
# from django.dispatch import receiver
# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm

# class WorkListCreateView(generics.ListCreateAPIView):
#     queryset = Work.objects.all()
#     serializer_class = WorkSerializer
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]

#     def get_queryset(self):
#         queryset = Work.objects.all()

#         # Filtering by work type
#         work_type = self.request.query_params.get('work_type', None)
#         if work_type:
#             queryset = queryset.filter(work_type=work_type)

#         # Searching by artist name
#         artist_name = self.request.query_params.get('artist', None)
#         if artist_name:
#             queryset = queryset.filter(artists__name__icontains=artist_name)

#         return queryset

#     def perform_create(self, serializer):
#         serializer.save(artist=self.request.user.artist)

#     def list(self, request, *args, **kwargs):
#         works = self.get_queryset()
#         serializer = WorkSerializer(works, many=True)
#         return Response(serializer.data)


# class ArtistListCreateView(generics.ListCreateAPIView):
#     queryset = Artist.objects.all()
#     serializer_class = ArtistSerializer

#     def create(self, request, *args, **kwargs):
#         form = ArtistRegistrationForm(request.data)
#         if form.is_valid():
#             user = form.save()

#             # Create an associated Artist object
#             artist = Artist.objects.create(user=user, name=form.cleaned_data['name'])

#             serializer = ArtistSerializer(artist)
#             headers = self.get_success_headers(serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#         else:
#             return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

#     def get_success_url(self):
#         return reverse_lazy('work-list-create')
    
#  # Make sure to replace this with the actual path to your serializer

# class RegisterView(generics.CreateAPIView):
#     serializer_class = UserCreationForm
#     permission_classes = [permissions.AllowAny]

#     def perform_create(self, serializer):
#         # Call save on the serializer, which will create the user
#         user = serializer.save()

#         # Create a token for the newly registered user
#         Token.objects.create(user=user)



# # class RegisterView(generics.CreateAPIView):
# #     serializer_class = UserCreationForm
# #     permission_classes = [permissions.AllowAny]

# #     def create(self, request, *args, **kwargs):
# #         response = super().create(request, *args, **kwargs)
# #         user = User.objects.get(username=request.data['username'])
# #         Token.objects.create(user=user)  # Create a token for the newly registered user
# #         return response
from rest_framework.authtoken.models import Token
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


