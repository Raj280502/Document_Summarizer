import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import requests
# Updated import to fix deprecation warning
from langchain_huggingface import HuggingFaceEmbeddings
from pinecone import Pinecone
from tqdm.auto import tqdm # A library to show a nice progress bar
import time
from langchain_pinecone import Pinecone
# Import the new, recommended class for Hugging Face models
from langchain_huggingface import HuggingFaceEndpoint
from langchain.chains import RetrievalQA
from dotenv import load_dotenv
from langchain_pinecone import PineconeVectorStore # Updated to use the newer class
from pinecone import Pinecone as PineconeClient # ADD THIS IMPORT


# Load environment variables from .env file
load_dotenv()


# We need to get these from the .env file
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
HUGGINGFACEHUB_API_TOKEN = os.getenv("HUGGINGFACEHUB_API_TOKEN")

INDEX_NAME = "document-summarizer-index"


def generate_summary_from_file(file_path):
    """
    This function takes a file path to a PDF, processes it, and returns a summary.
    """
    # Check if required environment variables are set
    print("--- TESTING PINECONE CONNECTION ---")
    if not PINECONE_API_KEY:
        print("ERROR: PINECONE_API_KEY not found in environment variables.")
        return "Server Configuration Error: Pinecone API Key is missing."
    try:
        pc = PineconeClient(api_key=PINECONE_API_KEY)
        print("Pinecone client initialized.")
        print("Existing indexes:", pc.list_indexes().names())
        print("Connection test successful.")
    except Exception as e:
        print(f"PINECONE CONNECTION FAILED: {e}")
        return f"Could not connect to Pinecone. Please check your API Key and network settings. Error: {e}"
    ### CONNECTION TEST END ###

    # Create a unique index name for this document to avoid conflicts
    import uuid
    unique_index_name = f"doc-{uuid.uuid4().hex[:8]}"
    print(f"Creating unique index: {unique_index_name}")

    try:
        # --- NEW: Use the filename as a unique namespace ---
        namespace = os.path.basename(file_path).replace('.pdf', '').replace('.', '_')
        print(f"Using namespace: {namespace}")

        # 1. Load the document
        loader = PyPDFLoader(file_path)
        documents = loader.load()
        print(f"Loaded {len(documents)} pages from PDF")

        # 2. Split the document into chunks
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        texts = text_splitter.split_documents(documents)
        print(f"Split into {len(texts)} text chunks")

        # 3. Initialize embeddings model
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        print("Embeddings model initialized")

        # 4. Create a fresh Pinecone index for this document
        print(f"Creating fresh index: {unique_index_name}")
        pc.create_index(
            name=unique_index_name,
            dimension=384,  # all-MiniLM-L6-v2 has 384 dimensions
            metric='cosine',
            spec={"serverless": {"cloud": "aws", "region": "us-east-1"}}
        )
        
        # Wait for index to be ready
        import time
        print("Waiting for index to be ready...")
        time.sleep(10)  # Wait for serverless index to be ready
        
        # 5. Initialize Pinecone vector store and add documents
        print("Creating vector store and adding documents...")
        
        # Use from_documents to create the vectorstore with all documents at once
        # Since we have a fresh index, we don't need a namespace
        vectorstore = PineconeVectorStore.from_documents(
            documents=texts,
            embedding=embeddings,
            index_name=unique_index_name
        )
        print(f"Added {len(texts)} documents to fresh vector store")
        
        # Wait a moment for indexing to complete
        print("Waiting for indexing to complete...")
        time.sleep(2)

        # 6. Initialize the Retriever
        # The vectorstore already knows about the namespace, so we don't need to specify it again
        retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

        ### DEBUGGING BLOCK START ###
        # Let's test what the retriever finds for a specific, simple query.
        test_query = "What is the main topic of this document?"
        # Use invoke instead of get_relevant_documents to fix deprecation warning
        try:
            retrieved_docs = retriever.invoke(test_query)
            print("--- DEBUGGING RETRIEVER ---")
            print(f"Found {len(retrieved_docs)} documents.")
            if len(retrieved_docs) == 0:
                print("WARNING: No documents retrieved! This means the vector store is empty or the retrieval failed.")
                # Try to check if the index has any vectors
                index = pc.Index(unique_index_name)
                stats = index.describe_index_stats()
                print(f"Index stats: {stats}")
            else:
                for i, doc in enumerate(retrieved_docs):
                    print(f"DOC {i+1}: {doc.page_content[:300]}...") # Print the first 300 chars
            print("---------------------------")
        except Exception as retrieval_error:
            print(f"ERROR during retrieval test: {retrieval_error}")
            return f"Retrieval test failed: {retrieval_error}"
### DEBUGGING BLOCK END ###
        

        # 7. Initialize the LLM
        repo_id = "meta-llama/Llama-3.1-8B"
        llm = HuggingFaceEndpoint(
            model=repo_id,
            temperature=0.1,
            max_new_tokens=512,
            huggingfacehub_api_token=HUGGINGFACEHUB_API_TOKEN
        )

        # 8. Create the RetrievalQA Chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=retriever,
            return_source_documents=False  # We only need the summary
        )
        
        # 9. Define the query and run the chain
        query = "Based on the provided document content, write a detailed and accurate summary that captures the main ideas, key findings, and important conclusions. Be specific about the actual content of the document."
        
        # Check if we have any retrieved documents before proceeding
        test_docs = retriever.invoke("summary")
        if len(test_docs) == 0:
            return "Error: No document content was found in the vector store. The PDF may not have processed correctly or the content may be unreadable."
        
        result = qa_chain.invoke(query)
        print(f"Generated summary length: {len(result['result'])} characters")

        # Clean up: delete the temporary index
        try:
            print(f"Cleaning up temporary index: {unique_index_name}")
            pc.delete_index(name=unique_index_name)
            print("Temporary index deleted successfully")
        except Exception as cleanup_error:
            print(f"Warning: Could not delete temporary index: {cleanup_error}")

        return result["result"]
        
        # # Clean up by deleting the Pinecone index after we're done
        # # Note: In a real-world app, you might want to keep indexes for caching.
        # from pinecone import Pinecone as PineconeClient
        # pc = PineconeClient(api_key=PINECONE_API_KEY)
        # if index_name in pc.list_indexes().names():
        #     pc.delete_index(name=index_name)


    except Exception as e:
        print(f"An error occurred: {e}")
        # Try to clean up the temporary index if it was created
        try:
            if 'unique_index_name' in locals() and 'pc' in locals():
                print(f"Cleaning up temporary index due to error: {unique_index_name}")
                pc.delete_index(name=unique_index_name)
        except:
            pass  # Ignore cleanup errors
        return f"An error occurred during summarization: {e}"

