import os
import time
import hashlib
from typing import Optional
from dotenv import load_dotenv, find_dotenv
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

# Setup
load_dotenv(find_dotenv())
DB_NAME = os.getenv("CLOUDANT_DB_NAME")


def get_client():
    apikey = os.getenv("CLOUDANT_API_KEY")
    url = os.getenv("CLOUDANT_URL")
    authenticator = IAMAuthenticator(apikey)
    client = CloudantV1(authenticator=authenticator)
    client.set_service_url(url)
    return client


# Pivate Utils
def _generate_id(unique_string: str):
    """Generates a unique ID from a string (like a URL) to prevent duplicates."""
    return hashlib.md5(unique_string.encode("utf-8")).hexdigest()


def _fetch_rev(doc_id: str):
    """Gets the latest revision ID (required for updates and deletes)."""
    client = get_client()
    doc = client.get_document(db=DB_NAME, doc_id=doc_id).get_result()
    return doc.get("_rev")


# News CRUD
def create_news(data: dict):
    """
    Saves news to Cloudant. 
    Uses a hash of the link as the ID to prevent duplicates.
    """
    if "link" in data:
        data["_id"] = _generate_id(data["link"])

    # Ensure metadata exists (though Pydantic should provide it now)
    data.setdefault("type", "news")
    data.setdefault("timestamp", time.time())

    client = get_client()
    try:
        # We use PUT because we are providing a specific _id
        return client.put_document(
            db=DB_NAME, 
            doc_id=data["_id"], 
            document=data
        ).get_result()
    except Exception as e:
        # Check if the error is a 409 (Document Conflict)
        if "409" in str(e):
            return {"status": "skipped", "message": "Duplicate entry (link already exists)"}
        return {"error": str(e)}


from typing import Optional

def read_news(limit: int = 100, unread_only: Optional[bool] = None):
    """
    Fetches news articles.
    - If unread_only is None: returns all news.
    - If unread_only is True: returns only news where is_read is False.
    - If unread_only is False: returns only news where is_read is True.
    """
    client = get_client()
    selector = {"type": "news"}
    
    if unread_only is True:
        selector["is_read"] = False
    elif unread_only is False:
        selector["is_read"] = True
        
    return (
        client.post_find(
            db=DB_NAME, 
            selector=selector, 
            limit=limit,
            sort=[{"timestamp": "desc"}] # Keeps newest news at the top
        )
        .get_result()
        .get("docs", [])
    )

def update_news(doc_id: str, update_data: dict):
    client = get_client()
    doc = client.get_document(db=DB_NAME, doc_id=doc_id).get_result()
    doc.update(update_data)
    return client.put_document(db=DB_NAME, doc_id=doc_id, document=doc).get_result()


def delete_news(doc_id: str):
    client = get_client()
    rev = _fetch_rev(doc_id)
    return client.delete_document(db=DB_NAME, doc_id=doc_id, rev=rev).get_result()


# Verified CRUD
def create_verified(data: dict):
    data["type"] = "verified"
    data["timestamp"] = time.time()
    return get_client().post_document(db=DB_NAME, document=data).get_result()


def read_verified(limit: int = 100):
    selector = {"type": "verified"}
    return (
        get_client()
        .post_find(db=DB_NAME, selector=selector, limit=limit)
        .get_result()
        .get("docs", [])
    )


def update_verified(doc_id: str, update_data: dict):
    client = get_client()
    doc = client.get_document(db=DB_NAME, doc_id=doc_id).get_result()
    doc.update(update_data)
    return client.put_document(db=DB_NAME, doc_id=doc_id, document=doc).get_result()


def delete_verified(doc_id: str):
    rev = _fetch_rev(doc_id)
    return get_client().delete_document(db=DB_NAME, doc_id=doc_id, rev=rev).get_result()


# Alerts CRUD
def create_alert(data: dict):
    data["type"] = "alert"
    data["active"] = data.get("active", True)
    data["timestamp"] = time.time()
    return get_client().post_document(db=DB_NAME, document=data).get_result()


def read_alerts(limit: int = 100, active_only: Optional[bool] = None):
    """
    Fetches alerts. 
    - If active_only is None: returns all alerts (history + active).
    - If active_only is True/False: filters accordingly.
    """
    client = get_client()
    selector = {"type": "alert"}
    
    if active_only is not None:
        selector["active"] = active_only
        
    return (
        client.post_find(
            db=DB_NAME, 
            selector=selector, 
            limit=limit,
            sort=[{"timestamp": "desc"}]
        )
        .get_result()
        .get("docs", [])
    )


def update_alert(doc_id: str, update_data: dict):
    client = get_client()
    doc = client.get_document(db=DB_NAME, doc_id=doc_id).get_result()
    doc.update(update_data)
    return client.put_document(db=DB_NAME, doc_id=doc_id, document=doc).get_result()


def delete_alert(doc_id: str):
    rev = _fetch_rev(doc_id)
    return get_client().delete_document(db=DB_NAME, doc_id=doc_id, rev=rev).get_result()
