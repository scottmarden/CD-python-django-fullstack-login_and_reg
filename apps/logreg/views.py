# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User

# Create your views here.
def index(request):
	if 'user_id' in request.session:
		return redirect('/success')
	return render(request, 'logreg/index.html')

def login(request):
	result = User.objects.login(request.POST)
	if isinstance(result, list):
		for err in result:
			messages.add_message(request, messages.ERROR, err)
		return redirect('/')
	else:
		request.session['user_id'] = result.id
		request.session['action'] = " logged in!"
		return redirect('/success')

def register(request):
	result = User.objects.register(request.POST)
	if isinstance(result, list):
		for err in result:
			messages.add_message(request, messages.ERROR, err)
		return redirect('/')
	else:
		request.session['user_id'] = result.id
		request.session['action'] = " registered!"
		return redirect('/success')

def success(request):
	if 'user_id' not in request.session:
		return redirect('/')
	print request.session['user_id']
	user = User.objects.get(id = request.session['user_id'])
	print user
	context = {
		'username': user.first_name,
		'action': request.session['action']
	}
	return render(request, 'logreg/success.html', context)

def logout(request):
	request.session.flush()
	return redirect('/')
