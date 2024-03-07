from Bio import Entrez

# Always provide your email address here
Entrez.email = "your_email@example.com"

def search_pubmed(query):
    # Use the esearch function to search the PubMed database
    handle = Entrez.esearch(db="pubmed", term=query, retmax=10)
    record = Entrez.read(handle)
    handle.close()

    # Get the list of Ids
    id_list = record["IdList"]
    return id_list

def fetch_details(id_list):
    ids = ','.join(id_list)
    handle = Entrez.efetch(db="pubmed", id=ids, retmode="xml")
    records = Entrez.read(handle)
    handle.close()
    return records

if __name__ == "__main__":
    query = "COVID-19"
    id_list = search_pubmed(query)
    articles = fetch_details(id_list)
    
    # Example of parsing some information
    for article in articles['PubmedArticle']:
        title = article['MedlineCitation']['Article']['ArticleTitle']
        abstract = article['MedlineCitation']['Article']['Abstract']['AbstractText'][0]
        print(f"Title: {title}")
        print(f"Abstract: {abstract}\n")
