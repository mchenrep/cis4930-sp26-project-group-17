def main():
    import requests
    
    # Set up base url and parameters
    BASE_URL = "https://api.github.com/search/repositories"
    params = {"q": "basketball", "per_page": 10, "page": 1} # 10 pages per run
    
    # Safely get response from API
    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status() # raise for errors
        data = response.json()
        
        '''
        5 meaningful fields we could possibly use:
            1. Stars
            2. Language
            3. Username
            4. Date created
            5. Open issues count

            Example down below:
        '''
        item = data["items"][0]
        record = {
            "stars": item.get("stargazers_count", 0),
            "language": item.get("language", "Unknown"),
            "username" : item.get("owner.login", "Unknown"),
            "date_created": item.get("created_at", "Unknown"),
            "open_issues" : item.get("open_issues_count", 0)
        }

    except requests.exceptions.Timeout:
        print("Request timed out")
    except requests.exceptions.RequestException as e:
        print("Request error:", e)  

if __name__ == "__main__":
    main()