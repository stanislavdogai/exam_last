from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from webapp.models import Ad

class PublicAd(APIView):
    def get(self, request, *args, **kwargs):
        ad = Ad.objects.get(pk=kwargs['pk'])
        ad.status = 'public'
        ad.save()
        return Response(data={'message' : 'Успешно опубликовано'})

class CancelAd(APIView):
    def get(self, request, *args, **kwargs):
        ad = Ad.objects.get(pk=kwargs['pk'])
        ad.status = 'cancel'
        ad.save()
        return Response(data={'message' : 'Отклонено'})