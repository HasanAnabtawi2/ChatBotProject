import json
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from Services.VectorDatabaseService import VectorDatabaseService




router=APIRouter()






@router.post("/chroma_add_by_url")
async def vector(vector_service:VectorDatabaseService=Depends(VectorDatabaseService),urls:List[str]=None):
    try:
        response=vector_service.add_document_by_urls(urls)

        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


@router.post("/load_url")
async def vector(vector_service:VectorDatabaseService=Depends(VectorDatabaseService),urls:List[str]=None):

    try:

        response=vector_service.url_loader(urls)

        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))





@router.get("/chroma_get_all")
async def vector(vector_service:VectorDatabaseService=Depends(VectorDatabaseService)):

    try:
        response=vector_service.get_all()

        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


@router.post("/semantic_search")
async def vector(vector_service:VectorDatabaseService=Depends(VectorDatabaseService),query:str=None,number_of_results:int=None):

    try:

        response=vector_service.get_documents_by_query(query,number_of_results)

        return response['documents']
    
    except Exception as e:
        return e
        