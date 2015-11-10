#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":

    os.environ.setdefault("DJANGO_SETTINGS_MODULE", 
                          "quest_maker.settings.settings_prod")

    this_machine = os.environ.get("MACHINE", None)
    if this_machine == 'local':
        os.environ["DJANGO_SETTINGS_MODULE"] = "quest_maker.settings.settings_dev"

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)