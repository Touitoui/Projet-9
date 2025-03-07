from django.http import HttpResponse
from django.shortcuts import render
from ticket.models import Ticket

def hello(request):
    return HttpResponse('<h1>Hello Django!</h1>')