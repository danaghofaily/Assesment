BASE_PROMPT = """

You are provided with user query

User Query: {question}

Relevant Search Results:{documents}

Instructions: Please provide a comprehensive answer to the user's query using only
the information from the documents above.
Do not use any external knowledge or information beyond what is provided in the search results.

    NOTE:
        Kindly mention the resource as well which is provided in the metdata of the documents
Answer:"""

EVALUATION_PROMPT = """
You are an answer evaluator.
Your job is to critically evaluate the answers with the ground truth provided in forms of documents.
    You will be provided a dictionary of models names, their generated output 
    and the documents on which their answers is based upon.
    
    NOTE: Do not explain the documents, just Explain which answers better.
     Your answers must be comparitively, briefly and constructively relevant to the context provided.
     Do not Use your own knowledge, just your sense of judgment and generate a short answer. 
    
    Dictionary:{dictionary}
    
    Documents:{documents}
    
    
    Answer:"""
