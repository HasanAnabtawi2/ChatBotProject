from typing import Annotated
from fastapi import APIRouter, Depends
from DTOs.PromptDTO import PromptDTO,PromptMessagesDTO
from Services.VectorDatabaseService import VectorDatabaseService
from Services.LlmService import LlmService


router=APIRouter()





@router.post("/rag_llm")
async def llm(prompt:PromptMessagesDTO,llm_service:LlmService=Depends(LlmService),vector_service:VectorDatabaseService=Depends(VectorDatabaseService)):

    documents=vector_service.get_documents_by_query(prompt.messages[len(prompt.messages)-1]["content"],2)
    response=llm_service.rag_llm_call(prompt.messages,documents)

    return response


@router.post("/llm")
async def llm(prompt:PromptDTO,llm_service:LlmService=Depends(LlmService)):

    
    response=llm_service.gpt(prompt.user_input)

    return response
