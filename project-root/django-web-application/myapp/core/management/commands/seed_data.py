from django.core.management.base import BaseCommand
from core.models import Repository, User, Language, NbaStat
import pandas as pd
import os
from django.conf import settings

class Command(BaseCommand):
    help = "Load CSV datasets into the database"
    
    def handle(self, *arg, **options):
        # 1. Load repository data
        repo_path = os.path.join(settings.BASE_DIR, "core", "data", "repos.csv")
        if os.path.exists(repo_path):
            df_repos = pd.read_csv(repo_path)
            repo_count = 0
            for _, row in df_repos.iterrows():
                # Get/create User
                user_obj, _ = User.objects.get_or_create(username=row["username"])
                
                # Get/create Language
                lang_obj = None
                if pd.notna(row["language"]):
                    lang_obj, _ = Language.objects.get_or_create(name=row["language"])
                
                # Clean date
                clean_date = None
                if pd.notna(row["date_created"]):
                    clean_date = str(row["date_created"]).split('T')[0]

                # Create repo
                _, created = Repository.objects.update_or_create(
                    repo_name=row["repo_name"],
                    owner=user_obj,
                    defaults={
                        "stars": int(row["stars"]),
                        "language": lang_obj,
                        "url": row["repo_url"],
                        "created_at": clean_date,
                        "source": "csv"
                    }
                )
                if created:
                    repo_count += 1
            self.stdout.write(self.style.SUCCESS(f"Successfully loaded {repo_count} new repositories."))
        else:
            self.stdout.write(self.style.WARNING(f"repos.csv not found at {repo_path}"))

        # 2. Load NBA Data (extending Project 1)
        nba_path = os.path.join(settings.BASE_DIR, "core", "data", "nba_processed.csv")
        if os.path.exists(nba_path):
            df_nba = pd.read_csv(nba_path)
            nba_count = 0
            for _, row in df_nba.iterrows():
                _, created = NbaStat.objects.get_or_create(
                    player=row["PLAYER"],
                    year=row["year_str"],
                    defaults={
                        "pts": float(row["PTS"]),
                        "eff": float(row["EFF"]),
                        "ast": float(row["AST"]),
                        "reb": float(row["REB"]),
                    }
                )
                if created:
                    nba_count += 1
            self.stdout.write(self.style.SUCCESS(f"Successfully loaded {nba_count} NBA records."))
        else:
            self.stdout.write(self.style.WARNING(f"nba_processed.csv not found at {nba_path}"))

        self.stdout.write(self.style.SUCCESS("Data seeding complete!"))