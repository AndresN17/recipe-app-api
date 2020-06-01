import time
from django.db import connections
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command that pause execution until database is avaliable"""

    def handle(self, *args, **options):
        self.stdout.write('waiting for database...')
        db_conn = None
        while not db_conn:
            try:
                db_conn = connections['default']
            except OperationalError:
                error_mess = "Database unavaliable, just wait 1 second..."
                self.stdout.write(error_mess)
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database avaliable'))
