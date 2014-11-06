from .models import Book
from django.contrib.auth.models import User
from .serializers import BookSerializer, UserSerializer
from rest_framework import generics
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from rest_framework import renderers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
#from django.http import Http404
#from rest_framework.views import APIView
#from rest_framework.response import Response
#from rest_framework import status


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


#4.read-only views for the user representations ListAPIView and RetrieveAPIView:
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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


""" # or use Class Based Views
class SnippetList(APIView):
    #List all books, or create a new snippet.
    def get(self, request, format=None):
        books = Snippet.objects.all()
        serializer = SnippetSerializer(books, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetSerializer(data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SnippetDetail(APIView):
    #Retrieve, update or delete a snippet instance.
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.DATA)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
"""
