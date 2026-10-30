import json
import requests
from datetime import datetime

# Fetch GitHub trending repos (simplified: use GitHub search API)
def fetch_repos(query='OCR model language:Python', sort='stars', order='desc'):
    url = 'https://api.github.com/search/repositories'
    params = {'q': query, 'sort': sort, 'order': order, 'per_page': 10}
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print('Error fetching repositories')
        return []
    return response.json()['items']

def extract_terms(repos):
    # Simple heuristic: extract repo names and descriptions as terms
    terms = {}
    for repo in repos:
        name = repo['name']
        desc = (repo.get('description') or '').lower().split()
        for word in desc:
            if word.isalnum() and len(word) > 3:
                terms[word] = terms.get(word, 0) + 1
        terms[name] = terms.get(name, 0) + 1
    return terms

def main():
    repos = fetch_repos()
    if not repos:
        return
    terms = extract_terms(repos)
    # Sort by frequency
    sorted_terms = sorted(terms.items(), key=lambda x: x[1], reverse=True)
    print(f"[{datetime.now().strftime('%Y-%m-%d')}] New OCR-related terms found:")
    for term, count in sorted_terms[:10]:
        print(f"- {term} (occurrences: {count})")

if __name__ == '__main__':
    main()
