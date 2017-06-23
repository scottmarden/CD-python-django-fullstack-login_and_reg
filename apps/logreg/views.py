# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
	return render(request, 'logreg/index.html')

def login(request):
	result = User.objects.login(request.POST)
	if isinstance(result, int):
		request.session['user_id'] = result
		request.session['action'] = "logged in!"
		return redirect('/success')
	else:
		for err in result:
			messages.add_message(request, messages.ERROR, err)
		return redirect('/')

def register(request):
	post_data = request.POST
	result = User.objects.validate(post_data)
	if isinstance(result, int):
		request.session['user_id'] = result
		request.session['action'] = "registered!"
		return redirect('/success')
	else:
		for err in result:
			messages.add_message(request, messages.ERROR, err)
		return redirect('/')

def success(request):
	print request.session['user_id']
	user = User.objects.get(id = request.session['user_id'])
	print user
	context = {
		'username': user.first_name,
		'action': request.session['action']
	}
	return render(request, 'logreg/success.html', context)
