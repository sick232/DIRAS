from src.services.vectorstore import get_vector_store

try:
    vs = get_vector_store()
    print(f"Vector store initialized successfully")
    print(f"Vector store type: {type(vs)}")
    
    # Try to get collection info
    if hasattr(vs, 'client'):
        collections = vs.client.list_collections()
        print(f"\nCollections: {len(collections)}")
        for col in collections:
            print(f"  - {col.name if hasattr(col, 'name') else col}")
    
    # Try to count embeddings
    if hasattr(vs, 'search'):
        print("\nVectorstore has search method")
    
    # Get direct ChromaDB info
    import chromadb
    from src.shared.config import settings
    chroma_path = settings.chroma_db_path
    print(f"\nChroma DB path: {chroma_path}")
    
    from pathlib import Path
    if Path(chroma_path).exists():
        print(f"Chroma DB path exists")
        # List files
        for f in Path(chroma_path).iterdir():
            print(f"  - {f.name}")
    else:
        print(f"Chroma DB path does NOT exist")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
