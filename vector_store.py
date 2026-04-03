import chromadb
from sentence_transformers import SentenceTransformer 

class VectorManager:
    def __init__(self):
         
         # We'll use this to let the user know the model is being set up
         print("Initializing the embedding model...")

         # Using a multilingual model to ensure Arabic text is handled correctly
         self.encoder = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

         
         self.client = chromadb.PersistentClient(path="./chroma_db")

         # Creating or getting the collection where we will store our processed chunks
         self.collection = self.client.get_or_create_collection(name="my_documents")

    def add_chunks_to_db(self, chunks):
         
         """
        Takes a list of text chunks, converts them to embeddings, 
        and stores them in the vector database with unique IDs.
        """
         
         ids = [f"chunk_{i}" for i in range(len(chunks))] # Generate unique IDs for each chunk based on its index

         embeddings = self.encoder.encode(chunks).tolist() # Convert our text pieces into numerical vectors (embeddings)

         self.collection.add(
            documents=chunks,
            embeddings=embeddings,
            ids=ids
        )
    def search(self, query_text, n_results=3):
         
         """
        Converts the user's question into a vector and finds the 
        most relevant chunks from the database.
        """
         
         query_embedding = self.encoder.encode([query_text]).tolist()
         results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
         return results['documents'][0] # Return the actual text of the matching chunks
         