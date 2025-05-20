from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

class Command(BaseCommand):
    help = 'Apply migrations to all databases including shards'

    def handle(self, *args, **kwargs):
        shard_dbs = [key for key in settings.DATABASES if key.startswith('shard_')]
        default_db = 'default'

        # First apply to default
        self.stdout.write(f"Applying migrations on {default_db}")
        call_command('migrate', database=default_db)

        for db in shard_dbs:
            self.stdout.write(f"Applying migrations on {db}")
            call_command('migrate', database=db)
