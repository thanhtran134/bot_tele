
import openai
import weaviate
import http.client
from fastapi import FastAPI, HTTPException
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Weaviate
from pydantic import BaseModel
from weaviate.classes.init import Auth
from app.setting import OPENAI_API_KEY, WEAVIATE_URL, WEAVIATE_API_KEY
from bot import bot
if __name__ == "__main__":
    # Initialize Weaviate client
    client = weaviate.connect_to_weaviate_cloud(
        cluster_url=WEAVIATE_URL,  # Replace with your Weaviate Cloud URL
        auth_credentials=Auth.api_key(WEAVIATE_API_KEY),  # Replace with your Weaviate Cloud key
        headers={'X-OpenAI-Api-key': OPENAI_API_KEY},
        skip_init_checks=True # Replace with your OpenAI API key
    )

