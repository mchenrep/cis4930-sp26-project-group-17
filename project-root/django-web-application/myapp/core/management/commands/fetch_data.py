import requests
import time
from django.core.management.base import BaseCommand
from core.models import Repository, User, Language

BASE_URL = "https://api.github.com/search/repositories"

class Command(BaseCommand):
    help = "Fetch GitHub repos and save directly to the database via ORM"

    def handle(self, *args, **options):
        query = "basketball"
        per_page = 10
        max_pages = 5
        page = 1
        total_saved = 0

        self.stdout.write(f"Fetching data from GitHub API: '{query}'...")

        while page <= max_pages:
            params = {"q": query, "per_page": per_page, "page": page}
            max_retries = 1
            success = False
            
            for attempt in range(max_retries + 1):
                try:
                    response = requests.get(BASE_URL, params=params, timeout=10)
                    response.raise_for_status()
                    data = response.json()
                    items = data.get("items", [])

                    if not items:
                        break

                    # Save to database (via ORM)
                    for item in items:
                        # 1. Get/create User
                        owner_data = item.get("owner", {})
                        user_obj, _ = User.objects.get_or_create(
                            username=owner_data.get("login", "Unknown")
                        )
                        
                        # 2. Get/create Language
                        lang_obj = None
                        lang_name = item.get("language")
                        if lang_name:
                            lang_obj, _ = Language.objects.get_or_create(name=lang_name)

                        # 3. Update/create Repository
                        repo_name = item.get("name", "Unknown")
                        Repository.objects.update_or_create(
                            repo_name=repo_name,
                            owner=user_obj,
                            defaults={
                                "stars": item.get("stargazers_count", 0),
                                "language": lang_obj,
                                "url": item.get("html_url", "Unknown"),
                                "created_at": item.get("created_at", "Unknown")[:10] if item.get("created_at") else None,
                                "source": "api" # Marking as source for API
                            }
                        )
                        total_saved += 1

                    page += 1
                    success = True
                    break

                except requests.exceptions.Timeout:
                    self.stdout.write(f"Timeout on page {page} (Attempt {attempt + 1}/{max_retries + 1})")
                    if attempt < max_retries:
                        time.sleep(2)
                except requests.exceptions.RequestException as e:
                    self.stdout.write(self.style.ERROR(f"Request error: {e}"))
                    break 

            if not success:
                self.stdout.write(self.style.WARNING("Skipping page due to repeated errors."))
                break

        self.stdout.write(self.style.SUCCESS(f"Successfully fetched and saved {total_saved} repositories to database"))