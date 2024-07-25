from decouple import config
OPENAI_API_KEY = config('OPENAI_API_KEY')

# Document loading and parsing.
import bs4
from langchain_community.document_loaders import WebBaseLoader

def load_almanac(filepath):
    urls = open(filepath, 'r').read().splitlines()
    urls = [urls[0]]

    # Only keep post title, headers, and content from the full HTML.
    strainer = bs4.SoupStrainer(class_=("field--name-field-body", 
                                        "field--name-field-planting", 
                                        "field--name-field-care", 
                                        "field--name-field-harvest",
                                        "field--name-field-wit-and-wisdom",
                                        "field--name-field-pests",
                                        "field--name-field-cooking-notes"))
    loader = WebBaseLoader(
        web_paths=urls,
        bs_kwargs={"parse_only": strainer},
    )

    docs = loader.load()
    return docs

def main():
    documents = load_almanac("./almanac_urls.txt")
    print(documents[0])

if __name__ == '__main__':
    main()