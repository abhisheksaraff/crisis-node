import sys
import json
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

backend_path = root / "backend"
sys.path.insert(0, str(backend_path))

from data.db import read_news 
from app.schemas.news import NewsEntry 

def test_fetch_all():
    print("\n" + "="*60)
    print("      CRISIS-NODE DATABASE DUMP")
    print("="*60)
    
    try:
        raw_data = read_news(limit=100)
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return

    if not raw_data:
        print("Empty Database: No documents found with type='news'")
        return

    for i, doc in enumerate(raw_data, 1):
        print(f"\n[#{i}] {doc.get('title', 'UNTITLED')}")
        print("-" * 30)
        
        # Print all fields in the document
        for key, value in doc.items():
            # Skip the huge content field for readability, just show length
            if key == "content" and value:
                print(f"  {key}: ({len(value)} characters)")
            else:
                print(f"  {key}: {value}")

    print("\n" + "="*60)
    print(f"TOTAL ARTICLES RETRIEVED: {len(raw_data)}")
    print("="*60)

if __name__ == "__main__":
    test_fetch_all()