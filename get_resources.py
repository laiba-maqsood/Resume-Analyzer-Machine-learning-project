import requests

API_KEY = "Your API"  
SEARCH_ENGINE_ID = "Your ID"  

def search_courses(skill):
    platforms = {
        'Coursera': 'site:coursera.org',
        'Udemy': 'site:udemy.com',
  
    }

    results = {}
    for platform, site in platforms.items():
        query = f"{skill} {site}"
        url = f"https://www.googleapis.com/customsearch/v1?q={query}&key={API_KEY}&cx={SEARCH_ENGINE_ID}"

        try:
            response = requests.get(url)
            data = response.json()
            links = []
            if "items" in data:
                for item in data["items"]:
                    links.append({
                        "title": item["title"],
                        "link": item["link"]
                    })
            results[platform] = links
        except Exception as e:
            print(f"Error fetching data for {platform}: {e}")
            results[platform] = []

    return results

if __name__ == "__main__":
    skill = "Python programming"
    resources = search_courses(skill)

    for platform, links in resources.items():
        print(f"\n{platform}:")
        if links:
            for link in links:
                print(f"  Title: {link['title']}")
                print(f"  URL: {link['link']}")
        else:
            print("  No resources found.")
