from django.shortcuts import render, render_to_response, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template import RequestContext


from models import Quest, User, UserQuest
from forms import RegistrationForm

# Create your views here.
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
        params = {
            "quest": quest,
            "user_info": user_info,
            "all_users_info": everyone_on_quest
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

    else:
        raise PermissionDenied

