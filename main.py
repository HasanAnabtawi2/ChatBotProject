from fastapi import FastAPI
import uvicorn
from routers import LLMRouter, VectorDbRouter
from fastapi.middleware.cors import CORSMiddleware






   

app = FastAPI()


 
 
 
 
 

 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
 


app.include_router(LLMRouter.router)
app.include_router(VectorDbRouter.router)




if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)