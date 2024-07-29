from decouple import config
import os
os.environ['OPENAI_API_KEY'] = config('OPENAI_API_KEY')
VS_ADDRESS = "https://rag-vector-store.search.windows.net"
VS_KEY = config('AZ_AIS_KEY')

# Vector store
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import OpenAIEmbeddings

# LLM
from langchain_openai import ChatOpenAI
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import WikipediaRetriever
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
    
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def test_index():
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

    gardening_retriever = vector_store.as_retriever(search_type="similarity")
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
    test_index()
