from typing import List
import chromadb
from langchain_text_splitters import CharacterTextSplitter
import ollama
from langchain_community.document_loaders import UnstructuredURLLoader
import uuid

from text_cleaning import clean_text


class VectorDatabaseService:

    
   
    def __init__(self):
      self.chroma_client=chromadb.PersistentClient()
      self.collection = self.chroma_client.get_or_create_collection(name="my_collection")
      
      

    def get_embedding(self,doc:str):
        vector=ollama.embeddings(
            model='nextfire/paraphrase-multilingual-minilm',
            prompt=doc
            
        )

        return vector.embedding 
    
    
            
    def add_document(self,documents:List[str]):

        vectors=[]
        ids=[]
        for doc in documents:
            vectors.append(self.get_embedding(doc))
            ids.append(str(uuid.uuid4()))


        self.collection.add(
            documents=documents,
            embeddings=vectors,
            ids=ids
            

        )


    def get_documents_by_vector(self,query_vector:list,number_of_results:int):
        results = self.collection.query(
        query_embeddings=query_vector,
        n_results=number_of_results,
        include=["embeddings","documents"]
    
        )
        return results
    

    def get_documents_by_query(self,query:str,number_of_results:int):

        query_vector=self.get_embedding(query)
        results = self.collection.query(
            query_embeddings=query_vector,
            n_results=number_of_results,
            include=["embeddings","documents"]

            )
        return results


    def get_all(self):
        results = self.collection.get( )
        return results
    

       
    def get_by_id(self,ids:list):
        result = self.collection.get( ids=ids )
        return result

    def url_loader(self,urls:List[str]):
            
            loader = UnstructuredURLLoader(urls=urls)
            data = loader.load()

            return data


    def character_text_split(self,document):
        text_splitter = CharacterTextSplitter(
            
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            is_separator_regex=False
        )

        splitted_list=[]
        splitted=text_splitter.split_text(document)
        for doc in splitted:
            splitted_list.append(clean_text(doc))
            
        return splitted_list
    
        




 
    def add_document_by_urls(self,urls:List[str]):

        
            
            
            documents=self.url_loader(urls)
            for document in documents:
                
                vectors=[]
                ids=[]
                metadata=[]
                splitted_documents=self.character_text_split(document.page_content )
                for doc in splitted_documents:
                    vectors.append(self.get_embedding(doc))
                    ids.append(str(uuid.uuid4()))
                    metadata.append(document.metadata)


                self.collection.add(
                    documents=splitted_documents,
                    embeddings=vectors,
                    ids=ids,
                    metadatas=metadata
                    

                )

    
    
 

            

    

        

        
        
      
    
       
       
      

      


