# right now, this can be copy-pasted into the django shell to seed
# TO DO: make this an actual script
# TO DO: make a script to load Walk to Rivendell?

from quest_maker_app.models import *
from django.utils import timezone
from datetime import datetime, timedelta, date

user1 = User(username="foobar", email="foo@bar.com", password="hello")
user1.set_password("hello")
user2 = User(username="mickey", email="mickey@bar.com", password="hello")
user2.set_password("hello")
user3 = User(username="jim", email="jim@bar.com", password="hello")
user3.set_password("hello")

user1.save()
user2.save()
user3.save()

quest_template = QuestTemplate(author_id=1, 
                               description="this is a super awesome quest template", 
                               name="sample quest template")
quest_template.save()

start = Waypoint(quest_template_id=1, 
                     notability="medium",
                     distance_from_start=0,
                     name="start",
                     description="this is the start")
waypoint1 = Waypoint(quest_template_id=1, 
                     notability="medium",
                     distance_from_start=2.0,
                     name="waypoint 1",
                     description="this is waypoint 1")
waypoint2 = Waypoint(quest_template_id=1, 
                     notability="high",
                     distance_from_start=4.0,
                     name="waypoint 2",
                     description="this is waypoint 1")
waypoint3 = Waypoint(quest_template_id=1, 
                     notability="low",
                     distance_from_start=7.0,
                     name="waypoint 3",
                     description="this is waypoint 1")
waypoint4 = Waypoint(quest_template_id=1, 
                     notability="medium",
                     distance_from_start=15.0,
                     name="waypoint 4",
                     description="this is waypoint 1")
start.save()
waypoint1.save()
waypoint2.save()
waypoint3.save()
waypoint4.save()

quest = Quest(template_id=1, 
              leader_id=1, 
              users_last_updated=timezone.now() - timedelta(days=1),
              start_date=date(2015, 7, 1),
              name="awesome quest",
              hours_offset_utc=0)
quest.save()

user_quest1 = UserQuest(character="foooo", total_miles=0, quest_id=1, user_id=1)
user_quest2 = UserQuest(character="me", total_miles=0, quest_id=1, user_id=2)

user_quest1.save()
user_quest2.save()
