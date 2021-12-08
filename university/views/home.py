from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, ListView, TemplateView, View
import requests
from django.shortcuts import render, get_object_or_404, redirect



class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        print(type(context))
        return context
