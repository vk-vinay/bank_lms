import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from bank.models import Account

# Create your views here.


def ping(request, date):
    print(date)
    return HttpResponse("Pong!", status=200)


@api_view(['POST'])
def deposit(request):
    try:
        a = Account.deposit(**request.data)
        return Response("Successful", status=status.HTTP_200_OK)
    except Exception as e:
        return HttpResponse(e.__str__(), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def withdraw(request):
    try:
        a = Account.withdraw(**request.data)
        return Response("Successful", status=status.HTTP_200_OK)
    except Exception as e:
        return HttpResponse(e.__str__(), status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def transfer(request):
    try:
        a = Account.transfer(**request.data)
        return Response("Successful", status=status.HTTP_200_OK)
    except Exception as e:
        return HttpResponse(e.__str__(), status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def report(request):
    try:
        data = Account.objects.prefetch_related('transaction_set').filter()
        return render(request, "report.html", context={"results": data})
    except Exception as e:
        return HttpResponse(e.__str__(), status=status.HTTP_400_BAD_REQUEST)
