from rest_framework import serializers
from .models import Book
from django.contrib.auth.models import User
"""
The first thing we need to get started on our Web API is to provide a way of serializing and
deserializing the snippet instances into representations such as json.
We can do this by declaring serializers that work very similar to Django's forms.
Create a file in the books directory named serializers.py and add the following
"""


class BookSerializer(serializers.HyperlinkedModelSerializer):
    #reflect user permissions on this class & add owner to fields of the inner Meta class
    owner = serializers.Field(source='owner.username')

    highlight = serializers.HyperlinkedIdentityField(view_name='book-highlight', format='html')

    class Meta:
        model = Book
        fields = ('url', 'highlight', 'owner',
                  'title', 'code', 'linenos', 'language', 'style')


#Adding endpoints for our User models
class UserSerializer(serializers.HyperlinkedModelSerializer):
    #books = serializers.PrimaryKeyRelatedField(many=True)
    books = serializers.HyperlinkedRelatedField(many=True, view_name='book-detail')

    class Meta:
        model = User
        fields = ('url', 'username', 'books')