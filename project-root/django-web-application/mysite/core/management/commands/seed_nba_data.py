from django.core.management.base import BaseCommand
from core.models import NbaStat
import pandas as pd
import os

class Command(BaseCommand):
    help = "Load NBA dataset from Project 1 into the database"

    def handle(self, *arg, **options):
        csv_path = "core/data/nba_processed.csv"

        if not os.path.exists(csv_path):
            self.stderr.write(f"File not found: {csv_path}")
            return

        df = pd.read_csv(csv_path)
        for _, row in df.iterrows():
            NbaStat.objects.get_or_create(
                player = row["PLAYER"],
                year = int(str(row["year"])[:4]),
                defaults = {
                    "team": row["TEAM"],
                    "gp": int(row["GP"]) if pd.notna(row["GP"]) else 0,
                    "pts": float(row["PTS"]) if pd.notna(row["PTS"]) else 0.0,
                    "ast": float(row["AST"]) if pd.notna(row["AST"]) else 0.0,
                    "reb": float(row["REB"]) if pd.notna(row["REB"]) else 0.0,
                    "eff": float(row["EFF"]) if pd.notna(row["EFF"]) else 0.0,
                }
            )
        self.stdout.write(self.style.SUCCESS("NBA Data loaded successfully"))