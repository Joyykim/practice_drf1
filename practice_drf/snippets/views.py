from django.db.models.signals import post_save
from django.dispatch import receiver
from django.shortcuts import render

# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
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
from django_filters import rest_framework as d_filters


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


class SnippetFilterSet(d_filters.FilterSet):
    min_price = d_filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = d_filters.NumberFilter(field_name="price", lookup_expr='lte')
    # price = d_filters.NumberFilter(field_name="price")
    published = d_filters.CharFilter(field_name='code', method='filter_startswith_code')

    def filter_startswith_code(self, queryset, name, value):
        title_filter = {f'{name}__startswith': value}
        return queryset.filter(**title_filter)

    class Meta:
        model = Snippet
        fields = ('price',)


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = (d_filters.DjangoFilterBackend,)
    filterset_class = SnippetFilterSet
