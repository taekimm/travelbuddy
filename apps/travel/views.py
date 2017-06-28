from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, TravelPlan
from django.core.urlresolvers import reverse
from django.db.models import Count

# Create your views here.

def index(request):
	return render(request, 'travel/index.html')

def register(request):
	result = User.objects.register(request.POST)
	if isinstance(result, int):
		#validation successful
		request.session['userid'] = result
		return redirect(reverse('home'))
	else:
		#unsuccessful, flash messages
		for error in result:
			messages.add_message(request, messages.ERROR, error)
		return redirect(reverse('loginandres'))

def login(request):
	try:
		result = User.objects.login(request.POST)
		if isinstance(result, int):
			#login successful
			request.session['userid'] = result
			return redirect(reverse('home'))
		else:
			#unsuccessful, flash messages
			for error in result:
				messages.add_message(request, messages.ERROR, error)
			return redirect(reverse('loginandres'))
	except:
		messages.add_message(request, messages.ERROR, 'User authentication failed')
		return redirect(reverse('loginandres'))

def logout(request):
	request.session.clear()
	return redirect(reverse('loginandres'))

def home(request):
	user = User.objects.get(id=request.session['userid'])
	usertravelplans = TravelPlan.objects.filter(planner=user)|TravelPlan.objects.filter(others=user)
	otherstravelplans = TravelPlan.objects.exclude(planner=user).exclude(others=user)
	context = {
		'user': user,
		'usertravelplans': usertravelplans,
		'otherstravelplans': otherstravelplans
	}
	return render(request, 'travel/travels.html', context)

def add(request):
	user = User.objects.get(id=request.session['userid'])
	return render(request, 'travel/add.html')

def add_plan(request):
	travelplan = TravelPlan.objects.create_plan(request.POST)
	if isinstance(travelplan, TravelPlan):
		return redirect(reverse('home'))
	else:
		for error in travelplan:
			messages.add_message(request, messages.ERROR, error)
		return redirect('/add')

def destination(request, TravelPlanID):
	travelplan = TravelPlan.objects.get(id=TravelPlanID)
	others = User.objects.filter(travel_plan__id=TravelPlanID)
	context = {
		'travelplan': travelplan,
		'others': others
	}
	return render(request, 'travel/destination.html', context)

def join(request, TravelPlanID):
	user = User.objects.get(id=request.session['userid'])
	travelplan = TravelPlan.objects.get(id=TravelPlanID)
	data={
		'travelplan': travelplan,
		'user': user
	}
	TravelPlan.objects.join_plan(data)
	return redirect(reverse('home'))

