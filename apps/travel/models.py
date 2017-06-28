# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

from dateutil.relativedelta import relativedelta
import re, bcrypt, datetime
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
	#register function
	def register(self, data):
		errors = []		
		#check on name length
		if len(data['name']) < 3:
			errors.append('Name must be longer than 3 character')
		
		#check on username length
		if len(data['username']) < 3:
			errors.append('Username must be longer than 3 character')
		
		#check if email is input
		if len(data['email']) < 1:
			errors.append('Email required')
		
		#email format check
		if not EMAIL_REGEX.match(data['email']):
			errors.append('Email must be in valid format')
		
		#password length check
		if len(data['password']) < 8:
			errors.append('Password must be 8 characters or longer')
		
		#password & password confirm check
		if data['password'] != data['confirm']:
			errors.append('Passwords must match') 
		
		#checking if passed error checks
		if len(errors) == 0:
			#using get to see if there are multiple users with said email
			#if .get() errors out, user with that email already exists.
			try:
				User.objects.get(email=data['email'])
				errors.append('User with that email already exists')
				return errors
			except: 
				user = User.objects.create(name=data['name'], username=data['username'], email=data['email'], password=bcrypt.hashpw(data['password'].encode(), bcrypt.gensalt()))
				return user.id
		else:
			return errors

	def login(self, data):
		errors = []
		if len(data['username']) < 1:
			errors.append('Username required')
		if len(data['username']) < 3:
			errors.append('Username must be longer than 3 character')
		#checking length of password
		if len(data['password']) < 8:
			errors.append('Password must be 8 characters or longer')
		#if no errors appened
		if len(errors) == 0:
			#try to get THE user - if the user does not exist, go to except
			try:
				user = User.objects.get(username__iexact=data['username'])
				encrypted_pw = bcrypt.hashpw(data['password'].encode(), user.password.encode())
				if encrypted_pw == user.password.encode():
					return user.id
			except: 
				errors.append('User authentication failed')
				return errors
		else:
			return errors

class User(models.Model):
	def __unicode__(self):
		return self.name
	
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add = True)
	updated_at = models.DateTimeField(auto_now = True)
	#to use UserManager
	objects = UserManager()

class TravelPlanManager(models.Manager):
	def create_plan(self, data):
		errors = []
		user = User.objects.get(id=data['userid'])
		if len(data['destination']) <= 0:
			errors.append('Please enter a destination')

		if len(data['plan']) <= 0:
			errors.append('Please enter a description')

		today = datetime.datetime.today()

		try:
			startdate = datetime.datetime.strptime(data['startdate'], '%Y-%m-%d')
			if startdate < today:
				errors.append('Travel plans cannot start in the past!')
		except:
			errors.append('Please enter a start date')

		try:
			enddate = datetime.datetime.strptime(data['enddate'], '%Y-%m-%d')
			if enddate < today:
				errors.append('Travel plans cannot end in the past!')
		except:
			errors.append('Please enter an end date')

		try:
			if startdate > enddate:
				errors.append('Please submit proof of Deloren if you are time traveling!')
		except:
			pass
		
		#checking if passed error checks
		if len(errors) == 0:
				travelplan = TravelPlan.objects.create(destination=data['destination'], startdate=data['startdate'], enddate=data['enddate'], plan=data['plan'], planner=user)
				return travelplan
		else:
			return errors

	def join_plan(self, data):
		user = data['user']
		travelplan = data['travelplan']
		travelplan.others.add(user)

class TravelPlan(models.Model):
	def __unicode__(self):
		return self.destination

	destination = models.CharField(max_length=255)
	startdate = models.DateField()
	enddate = models.DateField()
	plan = models.TextField()
	planner = models.ForeignKey(User)
	others = models.ManyToManyField(User, related_name="travel_plan")
	objects = TravelPlanManager()
