# This file's purpose is to use LangChain to index data for the Demeter RAG.
# We want to collect a set of data, then store it in Azure Cognitive Search as
# a vector store.

# References:
# https://python.langchain.com/v0.2/docs/tutorials/rag/#indexing
# https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.azuresearch.AzureSearch.html
from decouple import config
import os
os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')
VS_ADDRESS = "https://rag-vector-store.search.windows.net"
VS_KEY = config('AZ_AIS_KEY')

import tqdm

# Document loading and parsing.
import unicodedata
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Vector store
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import OpenAIEmbeddings


def load_almanac():
    urls = open("./urls/almanac.csv", 'r').read().splitlines()
    # Load HTML
    loader = AsyncChromiumLoader(urls)
    lazy_loader = loader.lazy_load()
    bs_transformer = BeautifulSoupTransformer()
    docs = []

    pbar = tqdm.tqdm(desc="Loading data from almanac.com", total=len(urls))
    with pbar:
        for html in lazy_loader:
            pbar.update(1)
        # Parse and filter HTML
        bs_transformer = BeautifulSoupTransformer()
        transformed_doc = bs_transformer.transform_documents(
            [html], 
            unwanted_tags=["footer", "iframe", "img", "header", "style", "scripts", "nav"],
            tags_to_extract=["p", "ul", "ol"],
            unwanted_classnames=["companion-planting-wrapper", "otPcPanel", 
                                 "ot-floating-button", "field field--name-field-credit", 
                                 "block-views-blockmore-like-this-block-2", "prod-rec",
                                 "global-header", "region--content-below", "advertisement-label", 
                                 "block-views-blockcomments-with-ajax--block-1",
                                 "region--highlighted grid-full", "site-branding__inner", 
                                 "ltkpopup-signup"],
            remove_lines=True,
            remove_comments=True
        )
        transformed_doc[0].page_content = unicodedata.normalize("NFKD", transformed_doc[0].page_content)
        docs.extend(transformed_doc)
    return docs

def load_bhg():
    urls = open("./urls/bhg.csv", 'r').read().splitlines()

    # Load HTML
    loader = AsyncChromiumLoader(urls)
    lazy_loader = loader.lazy_load()
    bs_transformer = BeautifulSoupTransformer()
    docs = []

    pbar = tqdm.tqdm(desc="Loading data from bhg.com", total=len(urls))
    with pbar:
        for html in lazy_loader:
            pbar.update(1)
        # Parse and filter HTML
        bs_transformer = BeautifulSoupTransformer()
        transformed_doc = bs_transformer.transform_documents(
            [html], 
            unwanted_tags=[],
            tags_to_extract=["p"],
            unwanted_classnames=[],
            remove_lines=True,
            remove_comments=True
        )
        transformed_doc[0].page_content = unicodedata.normalize("NFKD", transformed_doc[0].page_content)
        docs.extend(transformed_doc)
    return docs

def load_gardeners():
    urls = open("./urls/gardeners.csv", 'r').read().splitlines()

    # Load HTML
    loader = AsyncChromiumLoader(urls)
    lazy_loader = loader.lazy_load()
    bs_transformer = BeautifulSoupTransformer()
    docs = []

    pbar = tqdm.tqdm(desc="Loading data from gardeners.com", total=len(urls))

    with pbar:
        for html in lazy_loader:
            pbar.update(1)

            # Parse and filter HTML    
            transformed_doc = bs_transformer.transform_documents(
                [html], 
                unwanted_tags=["a", "footer"],
                tags_to_extract=["p"],
                unwanted_classnames=["alert-dialog-content__copy", "bottom-spacer", "article-search"],
                remove_lines=True,
                remove_comments=True
            )
            transformed_doc[0].page_content = unicodedata.normalize("NFKD", transformed_doc[0].page_content)
            docs.extend(transformed_doc)

    return docs

def create_vector_store():
    # Load documents
    docs = []
    docs.extend(load_almanac())
    docs.extend(load_bhg())
    docs.extend(load_gardeners())

    # Split text
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=200, add_start_index=True)
    all_splits = text_splitter.split_documents(docs)


    openai_api_version: str = "2023-05-15"
    model: str = "text-embedding-ada-002"
    embeddings = OpenAIEmbeddings(openai_api_version=openai_api_version, model=model)

    index_name = "rag-vector-store"
    vector_store = AzureSearch(
        azure_search_endpoint=VS_ADDRESS,
        azure_search_key=VS_KEY,
        index_name=index_name,
        embedding_function=embeddings.embed_query,
    )

    vector_store.add_documents(all_splits)

if __name__ == '__main__':
    create_vector_store()