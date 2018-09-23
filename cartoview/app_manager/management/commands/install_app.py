# -*- coding: utf-8 -*-
from __future__ import print_function

from django.core.management.base import BaseCommand

from cartoview.app_manager.installer import AppInstaller
from cartoview.app_manager.models import App, AppStore
from cartoview.log_handler import get_logger

logger = get_logger(__name__)


class Command(BaseCommand):
    help = 'Install App'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n', '--name', dest='name', help='Name Of The App To Install')
        parser.add_argument(
            '-av',
            '--app_version',
            type=str,
            dest='app_version',
            help='App Version')

    def handle(self, *args, **options):
        app_name = options.get('name')
        app_version = options.get('app_version')
        store = AppStore.objects.get(is_default=True)
        q = App.objects.filter(app_name=app_name)
        try:
            if q.count() == 0 and q.first().version < app_version:
                installer = AppInstaller(app_name, store.id, app_version)
                installer.install()
        except Exception as ex:
            logger.error(ex.message)
