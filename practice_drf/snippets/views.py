from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer


class SnippetViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving users.
    """

    def list(self, request):
        queryset = Snippet.objects.all()
        serializer = SnippetSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Snippet.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        serializer = SnippetSerializer(user)
        return Response(serializer.data)