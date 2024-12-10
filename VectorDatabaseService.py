import re
from typing import List
from bs4 import BeautifulSoup
import chromadb
import requests
import ollama
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_text_splitters import CharacterTextSplitter
import uuid


chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="my_collection")




def get_embedding(doc:str):
    vector=ollama.embeddings(
        model='nextfire/paraphrase-multilingual-minilm',
        prompt=doc
        
    )

    return vector.embedding 












def add_document(documents:List[str]):

    vectors=[]
    ids=[]
    for doc in documents:
        vectors.append(get_embedding(doc))
        ids.append(str(uuid.uuid4()))


    collection.add(
        documents=documents,
        embeddings=vectors,
        ids=ids
        

    )

def get_documents_by_vector(query_vector:list,number_of_results:int):
    results = collection.query(
    query_embeddings=query_vector,
    n_results=number_of_results,
    include=["embeddings","documents"]
   
    )
    return results






def character_text_split(document):
    text_splitter = CharacterTextSplitter(
        separator="\n\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len,
        is_separator_regex=False,
        
    )
    splitted_text=text_splitter.split_text(document)
    
    return splitted_text








urls=["https://www.tutorialsteacher.com/csharp/csharp-class",
]




def url_loader(urls:list):
    loader = UnstructuredURLLoader(urls=urls,)
    
    
    data = loader.load()

    
        
    return data
def get_documents_by_query(query:str,number_of_results:int):

        query_vector=get_embedding(query)
        results = collection.query(
            query_embeddings=query_vector,
            n_results=number_of_results,
            include=["embeddings","documents"]

            )
        return results

add_document(["Clases is blueprint","clases Used in OOP"])
query="class def?"
# query_vector=get_embedding(query)






results=get_documents_by_query(query,1)

print(results)












def add_document_by_urls(urls:List[str]):

      
        
        
        documents=url_loader(urls)

        

        for document in documents:
            vectors=[]
            ids=[]
            metadata=[]
            splitted_documents=character_text_split(document.page_content )
            for doc in splitted_documents:
                vectors.append(get_embedding(doc))
                ids.append(str(uuid.uuid4()))
                metadata.append(document.metadata)


            collection.add(
                documents=splitted_documents,
                embeddings=vectors,
                ids=ids,
                metadatas=metadata
                

            )







# result=get_documents_by_vector(query_vector,5)

# print(result)



def beautiful_soup_loader():
    url = "https://www.tutorialsteacher.com/csharp/csharp-class"

    response = requests.get(url)
    soup=BeautifulSoup(response.content,'html.parser')
    
    
    article=soup.find('article')
    
    
   
    print(article.get_text())



