from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Placeholder command for fetching external data."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Fetch command ready. Add API or CSV import logic here."))
