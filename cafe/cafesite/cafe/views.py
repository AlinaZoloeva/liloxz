from aiogram.utils.mixins import DataMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django import forms

from django.views.generic import FormView




def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about-us.html')


def contact(request):
    return render(request, 'contact-us.html')


def services(request):
    return render(request, 'our-services.html')

