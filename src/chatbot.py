from langchain_openai import ChatOpenAI
from langchain_community.llms import Replicate
from langchain_core.prompts import PromptTemplate
from langchain_openai import OpenAIEmbeddings
import os
from langchain_core.runnables import RunnablePassthrough
from dotenv import load_dotenv
from src.utils import return_vector_store, return_splitter
from src.prompts import EVALUATION_PROMPT, BASE_PROMPT
from langchain.retrievers.document_compressors import EmbeddingsFilter
from langchain.retrievers.document_compressors import DocumentCompressorPipeline
from langchain_community.document_transformers import EmbeddingsRedundantFilter
from langchain.retrievers import ContextualCompressionRetriever
from langchain_core.output_parsers import StrOutputParser

load_dotenv()


async def create_openai_chain(model_name: str):
    model = ChatOpenAI(model=model_name, temperature=0, streaming=True)
    prompt = PromptTemplate.from_template(template=BASE_PROMPT)
    lcel = ({
        "question": RunnablePassthrough(),
        "documents": RunnablePassthrough()
    }) | prompt | model | StrOutputParser()
    return lcel


async def create_replicate(model_name: str, model_kwargs: dict):
    os.environ["REPLICATE_API_TOKEN"] = "r8_OJ6ZPDnp4YntyYePWFJwvUWhsfZMTxr3Yk1Z2"
    model = Replicate(model=model_name, model_kwargs=model_kwargs, streaming=True,
                      replicate_api_token=os.getenv("REPLICATE_API_KEY"))
    prompt = PromptTemplate.from_template(template=BASE_PROMPT)
    lcel = ({
        "question": RunnablePassthrough(),
        "documents": RunnablePassthrough()
    }) | prompt | model | StrOutputParser()
    return lcel


class Chatbot:
    def __init__(self):
        self.evaluator = ChatOpenAI(model="gpt-4o", temperature=0)
        self.models = [
            {"name": "gpt-3.5-turbo"},
            {"name": "gpt-4"},
            {"name": "meta/llama-2-70b-chat", "model_kwargs": {"max_length": 4196, "temperature": 0.0}}
            # {"name": "joehoover/falcon-40b-instruct:7d58d6bddc53c23fa451c403b2b5373b1e0fa094e4e0d1b98c3d02931aa07173",
            #  "model_kwargs": {"max_length": 2048, "temperature": 0.1}
            #  },

        ]
        vector = return_vector_store()
        redundant_filter = EmbeddingsRedundantFilter(embeddings=OpenAIEmbeddings(model="text-embedding-3-large"))
        relevant_filter = EmbeddingsFilter(embeddings=OpenAIEmbeddings(model="text-embedding-3-large"),
                                           similarity_threshold=0.76)
        pipeline_compressor = DocumentCompressorPipeline(
            transformers=[return_splitter(), redundant_filter, relevant_filter]
        )
        self.retriever=vector.as_retriever()
        self.compression_retriever = ContextualCompressionRetriever(
            base_compressor=pipeline_compressor, base_retriever=self.retriever
        )
        self.results = {}
        evaluation = PromptTemplate.from_template(template=EVALUATION_PROMPT)
        self.evaluator_chain = ({
            "dictionary": RunnablePassthrough(),
            "documents": RunnablePassthrough()
        }) | evaluation | self.evaluator | StrOutputParser()

    async def get_docs(self, query: str):
        docs = await self.retriever.aget_relevant_documents(query)
        print(docs)
        return docs

    async def evaluate(self, docs):
        evaluation_input = {
            "dictionary": self.results,
            "documents": docs
        }
        evaluation_result = await self.evaluator_chain.ainvoke(evaluation_input)
        return evaluation_result
