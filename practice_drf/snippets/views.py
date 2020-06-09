from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import CursorPagination, LimitOffsetPagination, PageNumberPagination
from rest_framework.response import Response
from rest_framework.settings import api_settings

from snippets.models import Snippet
from snippets.serializers import SnippetSerializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

#
# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['code', ]
    #
    # def list(self, request):
    #     queryset = Snippet.objects.all()
    #     serializer = SnippetSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None):
    #     queryset = Snippet.objects.all()
    #     snippet = get_object_or_404(queryset, pk=pk)
    #     serializer = SnippetSerializer(snippet)
    #     return Response(serializer.data)
    #
    # # def create(self, request):
    # #     serializer = SnippetSerializer(request.data)
    # #     if serializer.is_valid():
    # #         serializer.save()
    # #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    # def create(self, request, *args, **kwargs):
    #     serializer = SnippetSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    #
    # def perform_create(self, serializer):
    #     serializer.save()
    #
    # def get_success_headers(self, data):
    #     try:
    #         return {'Location': str(data[api_settings.URL_FIELD_NAME])}
    #     except (TypeError, KeyError):
    #         return {}
    #
    # def update(self, request, pk=None):
    #     instance = Snippet.objects.get(pk=pk)
    #     serializer = SnippetSerializer(instance=instance, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #     return Response(serializer.data)
    #
    # def partial_update(self, request, pk=None):
    #     instance = Snippet.objects.get(pk=pk)
    #     serializer = SnippetSerializer(instance=instance, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #     return self.update(request, pk=pk)
    #
    # def destroy(self, request, pk=None):
    #     instance = Snippet.objects.get(pk=pk)
    #     instance.delete()
    #     return Response(status=status.HTTP_204_NO_CONTENT)
