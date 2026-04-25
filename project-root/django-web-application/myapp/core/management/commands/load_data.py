from django.core.management.base import BaseCommand
from core.models import Repository, User, Language
import pandas as pd


class Command(BaseCommand):
    help = "Load cleaned dataset into a database"

    def handle(self, *args, **options):
        df = pd.read_csv("core/data/repos.csv")

        for _, row in df.iterrows():

            # 1. Get or create related objects
            owner_obj, _ = User.objects.get_or_create(
                username=row["username"]
            )

            language_obj = None
            if pd.notna(row["language"]):
                language_obj, _ = Language.objects.get_or_create(
                    name=row["language"]
                )

            # 2. Create/update repository
            Repository.objects.update_or_create(
                repo_name=row["repo_name"],
                owner=owner_obj,   
                defaults={
                    "language": language_obj,
                    "stars": int(row["stars"]),
                    "url": row["repo_url"],
                    "created_at": row["date_created"] if pd.notna(row["date_created"]) else None,
                }
            )

        self.stdout.write(self.style.SUCCESS("Data loaded"))