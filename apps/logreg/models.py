# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
	def validate(self, data):
#if it doesn't match this, throw error
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
		NAME_REGEX = re.compile(r'^[0-9]+$')
		errors = []
#Are all fields populated?
		for item in data:
			if len(data[item]) < 1:
				print item + " is a required field"
#Name field verifications
		if len(data['first_name']) < 2 or len(data['last_name']):
			errors.append("First Name and Last Name must be at least 2 characters long")
		if NAME_REGEX.match(data['first_name']):
			errors.append("First name must contain only letters")
		if NAME_REGEX.match(data['last_name']):
			errors.append("Last name must contain only letters")
#email verifications
		if not EMAIL_REGEX.match(data['email']):
			errors.append("Please enter a valid email address")
		# add check for if email is already in database
#password verifications
		if data['password'] != data['confirm']:
			errors.append("Passwords did not match, please try again")
#no errors? register the user!
		if len(errors) == 0:
			user = User.objects.create(first_name=data['first_name'], last_name=data['last_name'], email=data['email'], password=data['password'])
			return user.id
#got errors? Go fix them!
		else:
			return errors

	def login(self, data):
		errors = []
		user_set = User.objects.filter(email=data['email'])
		if len(user_set) != 1:
			errors.append('Incorrect email address or password')
			return errors
		else:
			for user in user_set:
				return user.id

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_ad = models.DateTimeField(auto_now_add=True)
	updated_ad = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.first_name

	objects = UserManager()
