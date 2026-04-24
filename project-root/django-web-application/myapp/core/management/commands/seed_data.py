from django.core.management.base import BaseCommand
from core.models import Repository, User, Language
import pandas as pd

class Command(BaseCommand):
    help = "Load cleaned dataset into a database"
    
    def handle(self, *arg, **options):
        df = pd.read_csv("core/data/repos.csv")
        for _, row in df.iterrows():
            
            # 1. Get User object
            user_obj, created = User.objects.get_or_create(
                username=row["username"]
            )
            
            # 2. Get Language object
            lang_obj = None
            if pd.notna(row["language"]):
                lang_obj, created = Language.objects.get_or_create(
                    name=row["language"]
                )
            
            # 3. Clean data of the date
            clean_date = None
            if pd.notna(row["date_created"]):
                # Splits "2020-04-25T11:26:40Z" at the "T" and keeps "2020-04-25"
                clean_date = str(row["date_created"]).split('T')[0]
            
            # 4. Create Repo
            Repository.objects.update_or_create(
                repo_name=row["repo_name"],
                owner=user_obj,
                defaults={
                    "stars": int(row["stars"]),
                    "language": lang_obj,
                    "url": row["repo_url"],
                    "created_at": clean_date,  # Uses our new clean_date variable
                    "source": "csv"
                }
            )
        self.stdout.write(self.style.SUCCESS("GitHub Data loaded successfully!"))