# summarizer/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import DocumentSerializer
from .models import Document
from .service import generate_summary_from_file
import os
class SummarizeView(APIView):
    def post(self, request, *args, **kwargs):
        # Use the serializer to handle the file upload
        serializer = DocumentSerializer(data=request.data)
        
        if serializer.is_valid():
            document_instance = None
            try:
                # Save the document instance to get the file path
                saved_data = serializer.save()
                
                # Handle the case where save() might return a list
                if isinstance(saved_data, list):
                    document_instance = saved_data[0] if saved_data else None
                else:
                    document_instance = saved_data
                
                if not document_instance:
                    return Response(
                        {"error": "Failed to save document"},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
                
                # Get the full path to the saved file
                file_path = document_instance.file.path
                
                # Call our service function to get the summary
                summary = generate_summary_from_file(file_path)
                
                # Update the instance with the generated summary
                document_instance.summary = summary
                document_instance.save()
                
                # Return the updated data
                response_serializer = DocumentSerializer(document_instance)
                return Response(response_serializer.data, status=status.HTTP_200_OK)

            except Exception as e:
                # If summarization fails, try to delete the instance and return an error
                try:
                    if document_instance and hasattr(document_instance, 'delete'):
                        document_instance.delete()
                except:
                    pass  # If deletion fails, just continue
                
                # Get detailed error information
                error_details = f"{type(e).__name__}: {str(e)}"
                print(f"View error: {error_details}")
                
                import traceback
                traceback.print_exc()
                
                return Response(
                    {"error": f"An error occurred during summarization: {error_details}"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        else:
            # If the upload is invalid
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# summarizer/views.py

# ... (keep the existing imports and the SummarizeView class) ...
from .models import Document # Make sure this import is present

class AskView(APIView):
    def post(self, request, *args, **kwargs):
        # Get the document ID and the user's question from the request
        document_id = request.data.get('document_id')
        question = request.data.get('question')

        if not document_id or not question:
            return Response(
                {"error": "Document ID and question are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # Find the document in our database
            document = Document.objects.get(id=document_id)
            
            # Get the file path from the document instance
            file_path = document.file.path

            # --- This is where we would call a new service function for Q&A ---
            # For now, we'll build the logic directly here for simplicity.
            
            # 1. Initialize embeddings model
            from langchain_huggingface import HuggingFaceEmbeddings
            embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

            # 2. Connect to the existing Pinecone index using the file's namespace
            from langchain_pinecone import Pinecone as LangchainPinecone
            namespace = os.path.basename(file_path)
            vectorstore = LangchainPinecone.from_existing_index(
                index_name="document-summarizer-index", 
                embedding=embeddings,
                namespace=namespace
            )

            # 3. Create a retriever and the QA chain
            retriever = vectorstore.as_retriever(search_kwargs={"k": 5, "namespace": namespace})
            from langchain_huggingface import HuggingFaceEndpoint
            from langchain.chains import RetrievalQA
            
            repo_id = "meta-llama/Llama-3.1-8B"
            llm = HuggingFaceEndpoint(
                model=repo_id,
                temperature=0.1,
                max_new_tokens=512,
                huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_API_TOKEN")
            )

            qa_chain = RetrievalQA.from_chain_type(
                llm=llm,
                chain_type="stuff",
                retriever=retriever
            )

            # 4. Run the chain with the user's question
            answer = qa_chain.invoke(question)

            return Response({"answer": answer["result"]}, status=status.HTTP_200_OK)

        except Document.DoesNotExist:
            return Response({"error": "Document not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)