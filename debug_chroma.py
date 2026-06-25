from src.services.vectorstore import get_vector_store
import chromadb

try:
    # Get direct access to ChromaDB
    client = chromadb.PersistentClient(path="data/vectorstore")
    collection = client.get_collection(name="diras_documents")
    
    # Check count
    count = collection.count()
    print(f"Documents in collection: {count}")
    
    if count > 0:
        # Get first few entries
        all_data = collection.get()
        print(f"\nFirst 3 embeddings info:")
        for i in range(min(3, len(all_data['ids']))):
            print(f"  ID: {all_data['ids'][i]}")
            print(f"  Metadata: {all_data['metadatas'][i] if all_data['metadatas'] else 'None'}")
            doc_preview = all_data['documents'][i][:100] if all_data['documents'] else 'None'
            print(f"  Document preview: {doc_preview}...")
            print()
    else:
        print("No data in collection!")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
