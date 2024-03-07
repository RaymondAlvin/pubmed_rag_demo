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

def get_article_summaries(id_list):
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    ids = ','.join(id_list)
    params = {
        'db': 'pubmed',
        'id': ids,
        'retmode': 'json'
    }
    response = requests.get(base_url, params=params)
    summaries = response.json()
    return summaries  # You may want to parse this JSON to extract specific fields


def main():
    search_query = "caffeine AND health"
    article_ids = get_article_ids(search_query)
    if article_ids:
        summaries = get_article_summaries(article_ids)
        # Process and print summaries here. The structure of 'summaries' will depend on your specific needs.
        print(summaries)  # Placeholder for demonstration. You'll likely need to extract and format data from the JSON.

if __name__ == "__main__":
    main()

