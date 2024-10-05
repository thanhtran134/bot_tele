import weaviate
import os

from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import Weaviate
from weaviate.classes.init import Auth
from app.setting import WEAVIATE_URL, WEAVIATE_API_KEY, DATA_FOLDER_PATH,OPENAI_API_KEY
from langchain.text_splitter import RecursiveCharacterTextSplitter
import http.client

client = weaviate.Client(
    url=WEAVIATE_URL,

    auth_client_secret=weaviate.AuthApiKey(api_key=WEAVIATE_API_KEY),
    additional_headers={"X-OpenAI-Api-Key": OPENAI_API_KEY}
)
def get_text_splits(text_file):
  with open(text_file, 'r') as f:
    du_lieu = f.read()
    #chunk_size: used to break up text into smaller paragraphs (200 characters)
    #chunk_overlap: number of duplicate characters between paragraphs (20 characters)
    #length_function: use calculater length of text
    TextSplitter = RecursiveCharacterTextSplitter(chunk_size=80, chunk_overlap=20,length_function = len)
    doc_splits = TextSplitter.split_text(du_lieu)
  return doc_splits


def setup_weaviate_schema():
    schema = {
        "classes": [
            {
                "class": "People",
                "description": "A class to store articles from text files",
                "moduleConfig": {
                    "text2vec-openai": {
                        "model": "text-embedding-3-large",
                        "options": {
                            "waitForModel": True,
                            "useGPU": False,
                            "useCache": True
                        }
                    }
                },
                "properties": [
                    {
                        "name": "name_chr",
                        "dataType": ["text"],
                        "description": "Name about person"
                    },
                    {
                        "name": "content",
                        "dataType": ["text"],
                        "description": "Content about a person"
                    },
                ],
                "vectorizer": "text2vec-openai",

            },
        ]
    }

    return client.schema.create(schema)

folder_path = DATA_FOLDER_PATH
def upload_to_weaviate():
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)

            # Sử dụng hàm get_text_splits để tách file thành các đoạn nhỏ
            doc_splits = get_text_splits(file_path)

            # Xử lý từng đoạn nhỏ và thêm vào Weaviate
            for chunk in doc_splits:
                parts = chunk.strip().split(',')

                # Kiểm tra xem có đủ số phần tử để tránh lỗi
                if len(parts) >= 3:
                    name_chr = parts[0]
                    life = parts[1]

                    data_object = {
                        "name_chr": name_chr,
                        "content": chunk,
                        "life": life,
                    }
                    # Thêm đối tượng vào Weaviate
    client.data_object.create(data_object, "People")

def vectorDB_weaviate_setup():
    upload_to_weaviate()
    client.data_object.get(class_name="People", limit=2, with_vector=True)
    vectorstore = Weaviate(client, "People", "content", embedding=OpenAIEmbeddings(model='text-embedding-3-large'))
if __name__ == "__main__":
    setup_weaviate_schema()
    folder_path = DATA_FOLDER_PATH
    upload_to_weaviate()
    vectorDB_weaviate_setup()
