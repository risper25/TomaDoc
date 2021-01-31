from __future__ import unicode_literals
from django.apps import AppConfig


class DiagnoseConfig(AppConfig):
    name = 'diagnose'
    def ready(self):
    	import diagnose.signals



