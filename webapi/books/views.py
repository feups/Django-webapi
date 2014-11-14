from .models import Book
from .serializers import BookSerializer, UserSerializer
from .permissions import IsOwnerOrReadOnly
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import permissions, authentication
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
#from django.http import Http404
#from rest_framework.views import APIView
#from rest_framework.response import Response
#from rest_framework import status


#Session authentication
class BookList(generics.ListCreateAPIView):
    """
    CF: Sample Book list endpoint
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    #associate book with users
    def pre_save(self, obj):
        obj.owner = self.request.user

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


class BookDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    #associate book with users
    def pre_save(self, obj):
        obj.owner = self.request.user

    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)


#4.View Users only if Token is valid for ListAPIView and RetrieveAPIView:
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)  #
    permission_classes = (permissions.IsAuthenticated,)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
#5.add single endpoint for our api
@api_view(('GET',))
def web_api_root(request, format=None):
    """
    This is the rootpoint, you must choose where to go
    between links below.
    """
    return Response({
        'users': reverse('user-list', request=request, format=format),
        'books': reverse('book-list', request=request, format=format)
    })


#5.add a base class endpoint for the highlighted Book
class BookHighlight(generics.GenericAPIView):
    queryset = Book.objects.all()
    renderer_classes = (renderers.StaticHTMLRenderer,)

    def get(self, request, *args, **kwargs):
        book = self.get_object()
        return Response(book.highlighted)

