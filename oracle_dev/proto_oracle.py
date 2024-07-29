import tqdm
import os
from decouple import config
os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')

# Document loading and parsing.
import unicodedata
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Vector store
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

# LLM
from langchain_openai import ChatOpenAI
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import WikipediaRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

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

    vectorstore = Chroma.from_documents(documents=all_splits, embedding=OpenAIEmbeddings(), persist_directory="./chroma_db")
    docs = vectorstore.similarity_search("potato")

    return vectorstore


def get_vector_store():
    if os.path.exists("./chroma_db"):
        return Chroma(persist_directory="./chroma_db", embedding_function=OpenAIEmbeddings())
    else:
        return create_vector_store()

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def main():
    vectorstore = get_vector_store()
    gardening_retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 6})
    wikipedia_retreiver = WikipediaRetriever()
    retriever = EnsembleRetriever(retrievers=[gardening_retriever, wikipedia_retreiver], weights=[0.5,0.5])


    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")

    prompt = ChatPromptTemplate([
                ("system", "You are an helpful assistant named Demeter, designed answer questions about gardening. \
                    Use the following pieces of retrieved context to answer the question. \
                    If you don't know the answer, just say that you don't know. \
                    Use three sentences maximum and keep the answer concise. \n"),
                ("human", "Question: {question} \n Context: {context} \n Answer:"),
            ])
    
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser())

    while True:
        question = input("Input: ")
        print(rag_chain.invoke(question))


if __name__ == '__main__':
    main()