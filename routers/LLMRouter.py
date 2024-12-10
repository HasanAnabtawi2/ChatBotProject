from fastapi import APIRouter, Depends, HTTPException
from DTOs.PromptDTO import PromptDTO,PromptMessagesDTO
from Services.VectorDatabaseService import VectorDatabaseService
from Services.LlmService import LlmService


router=APIRouter()





@router.post("/rag_llm")
async def llm(prompt:PromptMessagesDTO,llm_service:LlmService=Depends(LlmService),vector_service:VectorDatabaseService=Depends(VectorDatabaseService)):

    try:
        documents=vector_service.get_documents_by_query(prompt.messages[len(prompt.messages)-1]["content"],2)
        response=llm_service.rag_llm_call(prompt.messages,documents)

        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))


@router.post("/llm")
async def llm(prompt:PromptDTO,llm_service:LlmService=Depends(LlmService)):

    try:
        response=llm_service.gpt(prompt.user_input)

        return response
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))