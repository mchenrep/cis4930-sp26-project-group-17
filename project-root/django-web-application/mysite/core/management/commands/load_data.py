from django.core.management.base import BaseCommand
from core.models import Repository
import pandas as pd

class Command(BaseCommand):
    help = "Load cleaned dataset into a database"
    
    def handle(self, *arg, **options):
        df = pd.read_csv("core/data/repos.csv")
        for _, row in df.iterrows():
            Repository.objects.update_or_create(
                repo_name = row["repo_name"],
                defaults = {
                    "username" : row["username"],
                    "stars" : int(row["stars"]),
                    "language" : row["language"],
                    "url": row["repo_url"],
                    "created_at": row["date_created"] if pd.notna(row["date_created"]) else None
                }
            )
        self.stdout.write(self.style.SUCCESS("Data loaded"))