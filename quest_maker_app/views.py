from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib import messages

from models import Quest, User, UserQuest, DailyDistance, Profile
from forms import (RegistrationForm, DailyDistanceFormDefaultDay,
    DailyDistanceForm)
from django.conf import settings

import datetime
from django.utils import timezone


def homepage(request):
    if request.user.is_authenticated():
        user = request.user
        quests = user.quest_set.all()

        params = {
            "user": user,
            "quests": quests
        }
        return render(request, 'quest_maker_app/user_home.html', params)
    else:
        return render(request, 'quest_maker_app/homepage.html', {})

def quest_template(request, quest_template_id):
    q_template = Quest.objects.get(id=quest_template_id)
    waypoints = sorted(
        q_template.waypoint_set.all(), key=lambda x: x.distance_from_start)

    params = {"q_template": q_template, "waypoints": waypoints}

    return render(request, 'quest_maker_app/quest_template_detail.html', params)

@csrf_protect
def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password1'],
                email=form.cleaned_data['email']
            )
            user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            profile = Profile(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'], user=user)
            profile.save()
            login(request, user)
            msg = ("Thanks for registering! You are now logged in and ready to "
                   "go questing.")
            messages.info(request, msg)
            return HttpResponseRedirect(reverse('quest_maker_app:homepage'))
    else:
        form = RegistrationForm()

    variables = RequestContext(request, {'form': form})

    return render_to_response('registration/signup.html', variables)

@csrf_protect
@login_required
def create_daily_distance(request):
    if request.method == 'POST':
        form = DailyDistanceForm(request.POST)
        new_daily_distance = form.save(commit=False)
        new_daily_distance.manually_entered = True
        new_daily_distance.user = request.user
        new_daily_distance.save()

        msg = ("You have added daily information for {}.".format(
            new_daily_distance.day))
        messages.info(request, msg)
        return HttpResponseRedirect(reverse('quest_maker_app:homepage'))
    else:
        day = request.GET.get('day')
        if day:
            day = datetime.datetime.strptime(day, "%Y-%m-%d").date()
            default_data = {"day": day}
            form = DailyDistanceFormDefaultDay(default_data)
        else:
            form = DailyDistanceForm()

    variables = RequestContext(request, {'form': form})
    variables.push({'day': day})
    return render_to_response('quest_maker_app/edit_daily_distance.html', 
        variables)

@csrf_protect
def update_daily_distance(request, daily_distance_id):
    daily_distance = DailyDistance.objects.get(pk=daily_distance_id)
    if daily_distance.user == request.user:
        if request.method == 'POST':
            form = DailyDistanceForm(
                request.POST, instance=daily_distance)
            new_daily_distance = form.save(commit=False)
            new_daily_distance.manually_entered = True
            new_daily_distance.save()

            msg = ("You have updated your daily information for {}.".format(
                new_daily_distance.day))
            messages.info(request, msg)
            # this should probably be smarter about redirecting
            return HttpResponseRedirect(reverse('quest_maker_app:homepage'))
        else:
            form = DailyDistanceFormDefaultDay(instance=daily_distance)

        variables = RequestContext(request, 
                                   {'form': form, 'day': daily_distance.day})
        return render_to_response('quest_maker_app/edit_daily_distance.html', 
            variables)
    else:
        raise PermissionDenied

@login_required
def quest(request, quest_id):
    user = request.user
    quest = Quest.objects.get(id=quest_id)
    # make sure user has access to quest
    if quest in user.quest_set.all():
        # update database at most once an hour
        now = timezone.now()
        mins_since_last_updated = (now - quest.users_last_updated).seconds / 60
        if mins_since_last_updated > 60:
            quest.update_from_fitbit()
        user_info = UserQuest.objects.get(user_id=user.id).get_info()

        everyone_on_quest = quest.get_users_info()
        yesterday = quest.latest_day
        params = {
            "quest": quest,
            "user_info": user_info,
            "all_users_info": everyone_on_quest,
            "yesterday": yesterday.strftime('%A, %B %-d')
        }
        return render(request, 'quest_maker_app/quest_detail.html', params)
    else:
        raise PermissionDenied


@login_required
def user_quest(request, quest_id, user_id):
    """
    Show details for a particular user on a particular quest
    """
    request_user = request.user
    quest = Quest.objects.get(id=quest_id)
    if quest in request_user.quest_set.all():
        user = User.objects.get(id=user_id)
        user_quest = UserQuest.objects.filter(user_id=user.id).get(
                                              quest_id=quest.id)
        
        params = {
            "username": user.username,
            "character": user_quest.character,
            "daily_info": user_quest.get_daily_info(),
            "quest": quest,
            "day_finished": user_quest.day_finished,
            "is_finished": user_quest.day_finished is not None,
            "is_request_user": request_user == user
        }
        return render(request, 'quest_maker_app/user_quest_detail.html', params)
    else:
        raise PermissionDenied


@login_required
def fitbit_signup(request):
    user = request.user
    is_fitbit_user = user.social_auth.exists()
    if not is_fitbit_user:
        return render(request, 'quest_maker_app/fitbit_signup.html', {})
    else:
        return redirect('quest_maker_app:homepage')
