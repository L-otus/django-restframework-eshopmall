from django.shortcuts import render
from django.http import HttpResponse
from app.qr_gen.oder_qr import order_generate
from app.qr_gen.models import order_qr
import requests
import json


# Create your views here.
def order(request):
    id=order_generate()
    locate=order_qr.objects.get(order_id=id)

