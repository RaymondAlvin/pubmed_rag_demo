import json
import requests

def get_article_ids(search_query):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        'db': 'pubmed',
        'term': search_query,
        'retmode': 'json',
        'retmax': 10  # Adjust based on how many results you want
    }
    response = requests.get(base_url, params=params)
    
    # Check the status code
    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        return []
    
    try:
        data = response.json()
    except ValueError as e:
        print("Failed to parse JSON response:", e)
        return []
        
    id_list = data['esearchresult']['idlist']
    return id_list

def get_article_content(article_id):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        'db': 'pubmed',
        'id': article_id,
        'rettype': 'medline',  # Change to 'medline' for full text, 'abstract for abstract'
        'retmode': 'text'
    }
    response = requests.get(base_url, params=params)
    return response.text

def main():
    search_query = "caffeine AND health"
    article_ids = get_article_ids(search_query)
    if article_ids:
        all_articles = []
        for article_id in article_ids:
            content = get_article_content(article_id)
            article_data = {
                'id': article_id,
                'content': content
            }
            all_articles.append(article_data)
        
        # Save article content to a JSON file
        with open('article_content.json', 'w') as json_file:
            json.dump(all_articles, json_file, indent=4)
        print("Article content saved to article_content.json")

if __name__ == "__main__":
    main()
