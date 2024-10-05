from langchain_community.chat_models import ChatOpenAI
from langchain.agents.agent_toolkits import create_retriever_tool
from langchain_community.vectorstores import Weaviate
from langchain.memory import ConversationBufferMemory
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from app.setting import OPENAI_API_KEY, WEAVIATE_URL, WEAVIATE_API_KEY
from langchain_community.embeddings import OpenAIEmbeddings
import weaviate
import os
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from fastapi import FastAPI
from weaviate.classes.init import Auth

os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=WEAVIATE_URL,  # Replace with your Weaviate Cloud URL
    auth_credentials=Auth.api_key(WEAVIATE_API_KEY),  # Replace with your Weaviate Cloud key
    headers={'X-OpenAI-Api-key': OPENAI_API_KEY}, # Replace with your OpenAI API key,
    skip_init_checks=True
)

# Set up Weaviate vector store
#add model embedding
vectorstore = Weaviate(client, "People", "content", embedding=OpenAIEmbeddings(model='text-embedding-3-large'))

def create_agent():
    # Create data retrieval toolS
    data_tool = create_retriever_tool(
        vectorstore.as_retriever(search_type="similarity_score_threshold", search_kwargs={"score_threshold": 0.3, "k": 3}),
        "info_information_retriever",
        "useful for when you need to answer questions about news"
    )
    # Define tools
    tools = [data_tool]
    # Initialize ChatOpenAI
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.4, openai_api_key=OPENAI_API_KEY)
    # Define system message
    message = SystemMessage(
        content=(
            "You are a helpful virtual advisor named MC."
        )
    )
    # Create agent
    memory = ConversationBufferMemory(llm=llm, memory_key="chat_history", max_token_limit=300)
    prompt = OpenAIFunctionsAgent.create_prompt(system_message=message)
    agent = OpenAIFunctionsAgent(llm=llm, tools=tools, prompt=prompt)
    return AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True)

message_history = ChatMessageHistory()
agent_with_chat_history = RunnableWithMessageHistory(
    create_agent(),
    # This is needed because in most real world scenarios, --------------------------------------a session id is needed
    # It isn't really used here because we are using a simple in memory ChatMessageHistory
    lambda session_id: message_history,
    input_messages_key="input",
    history_messages_key="chat_history",
)
client.close()

