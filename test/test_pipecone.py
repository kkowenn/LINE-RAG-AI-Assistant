import os
import logging
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec

logging.basicConfig(level=logging.INFO)

def init_pinecone():
    """
    Initialize the Pinecone client and connect to the specified index.
    """
    # Load environment variables
    load_dotenv()

    # Fetch environment variables
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_index_name = os.getenv("INDEX_NAME")
    pinecone_env = os.getenv("PINECONE_ENV", "us-east-1")

    if not pinecone_api_key or not pinecone_index_name:
        raise EnvironmentError("PINECONE_API_KEY and INDEX_NAME must be set in the environment.")

    # Initialize Pinecone client
    pc = Pinecone(api_key=pinecone_api_key, environment=pinecone_env)

    # Check if the index exists
    existing_indexes = pc.list_indexes()
    if pinecone_index_name not in existing_indexes:
        # Create the index if it does not exist
        pc.create_index(
            name=pinecone_index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud='aws', region=pinecone_env)
        )
        logging.info(f"Created new Pinecone index: {pinecone_index_name}")

    # Connect to the index
    index = pc.Index(pinecone_index_name)

    logging.info(f"Connected to Pinecone index: {pinecone_index_name}")

    return index
