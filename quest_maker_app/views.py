from django.shortcuts import render, render_to_response, get_object_or_404, redirect
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib.auth import authenticate, login
from django.contrib import messages

from models import Quest, User, UserQuest
from forms import RegistrationForm
from django.conf import settings

import datetime
import fitbit

FITBIT_KEY = settings.SOCIAL_AUTH_FITBIT_KEY
FITBIT_SECRET = settings.SOCIAL_AUTH_FITBIT_SECRET


def homepage(request):
    if request.user.is_authenticated():
        user = request.user
        quests = user.quest_set.all()

        params = {
            "user": user,
            "quests": quests
        }
        if user.social_auth.exists():
            # the user has attached a fitbit account
            user_tokens = user.social_auth.get().access_token
            user_key = user_tokens["oauth_token"]
            user_secret = user_tokens["oauth_token_secret"]
            authd_client = fitbit.Fitbit(FITBIT_KEY, FITBIT_SECRET, 
                resource_owner_key=user_key, resource_owner_secret=user_secret)
            distances = authd_client.time_series('activities/distance', period='7d')
            params["distances"] = distances
        return render(request, 'quest_maker_app/user_home.html', params)
    else:
        return render(request, 'quest_maker_app/homepage.html', {})

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
            login(request, user)
            msg = ("Thanks for registering! You are now logged in and ready to "
                   "go questing.")
            messages.info(request, msg)
            return HttpResponseRedirect(reverse('quest_maker_app:homepage'))
    else:
        form = RegistrationForm()

    variables = RequestContext(request, {'form': form})

    return render_to_response('registration/signup.html', variables)


@login_required
def quest(request, quest_id):
    # make sure user has access to quest
    user = request.user
    quest = Quest.objects.get(id=quest_id)
    if quest in user.quest_set.all():
        user_info = UserQuest.objects.get(user_id=user.id).get_info()

        everyone_on_quest = quest.get_latest_user_info()
        yesterday = datetime.date.today() - datetime.timedelta(1)
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
        user_quest = UserQuest.objects.filter(user_id=user.id).filter(
                                              quest_id=quest.id)
        params = {
            "username": user.username,
            "character": user_quest.character,
            "daily_info": user_quest.get_daily_info()
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

