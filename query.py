from openai import OpenAI
import os


client = OpenAI(
    # This is the default and can be omitted
    api_key=os.environ.get("OPENAI_API_KEY"),
)

def query_to_url(query):
    prompt = (
    "Format the following query into a PubMed search URL:\n"
    "User Input: \"Effects of caffeine on human health\"\n"
    "GPT-4 Output: https://pubmed.ncbi.nlm.nih.gov/?term=Effects+of+caffeine+on+human+health\n"
    f"Now format the following query into a PubMed Search URL: \"{query}\"")

    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    formatted_url = completion.choices[0].message.content
    return formatted_url

def get_query():
    user_query = input("Enter your pubmed search query: ")
    url = query_to_url(user_query)
    print(url)


if __name__ == "__main__":
    # client = OpenAI()
    get_query()