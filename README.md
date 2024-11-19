This project is about building a LINE chatbot integrated with a Retrieval-Augmented Generation (RAG) AI model, using Python and various libraries. Here are the key components and steps involved:

### Key Components:

1. **Flask Framework**: Used to create a web server that listens for incoming webhook events from LINE and handles requests.
2. **Pinecone**: A vector database used to store and query vectors (embeddings) representing text data. It helps in finding the most similar items in the database based on the input query.
3. **OpenAI GPT**: Used for generating chat responses and handling user interactions. The model uses the context and embeddings to generate relevant responses.
4. **Environment Variables**: Managed using `dotenv` to securely handle API keys and other configurations.

### Major Functionalities:

1. **Initialization**:

   - **Loading environment variables**: Using `dotenv` to securely manage keys and configurations.
   - **Pinecone Initialization**: Setting up the Pinecone client and connecting to an existing index or creating one if it does not exist.

2. **Webhook Handling**:

   - **Event Processing**: The `handle_webhook` function processes incoming events from LINE, dispatching them to appropriate handlers based on the event type.
   - **Message Handling**: Different handlers like `handle_text_message`, `handle_image_message`, etc., process specific types of messages. For text messages, embeddings are created, Pinecone is queried for similar results, and a response is generated using the GPT model.

3. **Embedding and Querying**:

   - **Embedding Generation**: `get_embeddings` function generates vector embeddings for the input text using OpenAI's embedding models.
   - **Pinecone Querying**: Query the Pinecone database to find the most similar vectors based on the input embeddings.

4. **Response Generation**:
   - **Chat Response**: Using OpenAI GPT to generate a contextual response based on the user's input and the retrieved similar items from Pinecone.

### Example Workflow:

1. A user sends a message to the LINE chatbot.
2. The webhook receives the message and triggers the appropriate handler.
3. For text messages, embeddings are generated and Pinecone is queried for similar items.
4. The results from Pinecone and the user's input are used to generate a response using OpenAI GPT.
5. The generated response is sent back to the user through the LINE messaging API.

step:
create `.env` in root directory of this project (you can use .env.example delete '.example'):

```plaintext
OPENAI_API_KEY=
CHANNEL_ID=
CHANNEL_SECRET=
PORT=
INDEX_NAME=
PINECONE_API_KEY=
PINECONE_ENV=
```

```bash
python main.py
```

```bash
ngrok http 3001
```

go setting in
