import os
import openai
import pinecone
from dotenv import load_dotenv
from pinecone_utils import init_pinecone

# Load environment variables
load_dotenv()

# Initialize OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Pinecone
pinecone_index = init_pinecone()

# Define a new namespace for the new data
namespace = "new_data"

# Read data from data.txt
def read_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

# Generate embeddings using OpenAI
def generate_embeddings(text):
    response = openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )
    return response['data'][0]['embedding']

# Upload embeddings to Pinecone
def upload_embeddings(index, data, namespace):
    vectors = []
    for i, text in enumerate(data):
        embedding = generate_embeddings(text)
        vectors.append({"id": f"vec_{i}", "values": embedding, "metadata": {"text": text}})
    index.upsert(vectors, namespace=namespace)

# Main function
if __name__ == "__main__":
    data = read_data("data.txt")
    upload_embeddings(pinecone_index, data, namespace)
    print("Data uploaded successfully!")
