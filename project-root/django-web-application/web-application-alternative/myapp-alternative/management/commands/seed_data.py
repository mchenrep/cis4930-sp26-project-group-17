from django.core.management.base import BaseCommand
from myapp.models import Item

class Command(BaseCommand):
    help = "Seed the database with sample Item records."

    def handle(self, *args, **options):
        sample_items = [
            {"name": "Sample Alpha", "category": "Demo", "description": "First sample item.", "value": 10.00},
            {"name": "Sample Beta", "category": "Demo", "description": "Second sample item.", "value": 20.00},
            {"name": "Sample Gamma", "category": "Test", "description": "Third sample item.", "value": 30.00},
        ]

        created = 0
        for item in sample_items:
            _, was_created = Item.objects.get_or_create(name=item["name"], defaults=item)
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"Seed complete. Created {created} item(s)."))
