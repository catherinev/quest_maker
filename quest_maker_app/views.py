from django.shortcuts import render, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

from models import Quest, User, UserQuest

import datetime


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

