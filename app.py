from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from src.chatbot import Chatbot, create_replicate, create_openai_chain
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str


async def generate_chat_responses(message, lcel, model_name, chat, docs):
    yield "\n\n"  # Start with two blank lines
    yield model_name + ": "
    if model_name == "joehoover/falcon-40b-instruct:7d58d6bddc53c23fa451c403b2b5373b1e0fa094e4e0d1b98c3d02931aa07173":
        docs = docs[:-2]
    response_chunks = []
    async for chunk in lcel.astream(input={"question": message, "documents": docs}):
        response_chunks.append(chunk)
        partial_response = ''.join(response_chunks)
        chat.results[model_name] = partial_response
        yield chunk
    yield "\n\n"

class QueryItem(BaseModel):
    query: str


@app.post("/query")
async def stream_response(query_item: QueryItem):
    query = query_item.query
    chat = Chatbot()
    chat.results = {}
    docs = await chat.get_docs(query=query)

    async def response_generator():
        for model in chat.models:
            if 'model_kwargs' in model:
                lcel = await create_replicate(
                    model_name=model["name"],
                    model_kwargs=model["model_kwargs"]
                )
            else:
                lcel = await create_openai_chain(model_name=model["name"])

            async for response in generate_chat_responses(query, lcel, model["name"], chat, docs):
                yield response

        yield "Evaluation by GPT4-Omni :"
        async for chunk in chat.evaluator_chain.astream(input={"documents": docs, "dictionary": chat.results}):
            yield chunk

    return StreamingResponse(response_generator(), media_type="text/plain")
