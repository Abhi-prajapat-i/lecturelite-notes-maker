import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_openrouter import ChatOpenRouter

load_dotenv()

'''
this model previous i have used but the token per minute of this model is 8k
but i am facing some problem then is used openrouter .
'''
# llm = ChatGroq(    
#     groq_api_key = os.getenv("GROQ_API_KEY"),
#     model_name = "openai/gpt-oss-120b"
# )

llm = ChatOpenRouter(
    openrouter_api_key = os.getenv("OPENROUTER_API_KEY"),
    model="google/gemma-4-31b-it",
    temperature=0,
)

# result = llm.invoke("what do you think about PM narendra Modi.")
# print(result.content)
