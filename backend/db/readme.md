# Database Guide

## Import Header

```
import sys
from pathlib import Path

# Move up to the crisis-node root
root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

# Add the backend folder to find schemas
sys.path.insert(0, str(root / "backend"))

from data.db import *
from app.schemas.news import NewsEntry
```

## Available Functions

### Read
```
# Options: unread_only=True (Inbox), unread_only=False (Archive), None (All)
news_items = read_news(limit=50, unread_only=True)

# Mark an item as read
from data.db import update_news
update_news("article_id_here", {"is_read": True})
```

```
verifications = read_verified(limit=100)
```

```
# 1. READ: Get all alerts (History + Active)
all_alerts = read_alerts(active_only=None)

# 2. READ: Get ONLY active alerts for the dashboard
active_alerts = read_alerts(active_only=True)

# 3. CREATE: Push a new alert
new_alert = {
    "event": "Flash Flood",
    "location": "Downtown Bridge",
    "severity": "Critical",
    "message": "Bridge closed. Seek alternate routes.",
    "active": True
}
create_alert(new_alert)
```

### Create
```
# 1. Define the data using the Schema
new_entry = NewsEntry(
    event="flood",
    title="Heavy Rain in Region",
    link="https://news.example.com/123"
)

# 2. Save it (Pass it as a dictionary using model_dump)
create_news(new_entry.model_dump())
```

```
create_verified({
    "source_id": "md5_hash_of_news_link",
    "status": "confirmed",
    "confidence_score": 0.98
})
```

```
alert_data = {
    "event": "Fire",
    "severity": "High",
    "message": "Evacuate North Sector",
    "active": True
}

create_alert(alert_data)
```

### Update or Delete
```
update_news(
    doc_id="67f0...", 
    update_data={"is_read": True}
)
```

```
delete_news("document_id_here")
```

```
# This keeps the alert in history but hides it from 'active' views
update_alert(
    doc_id="alert_uuid_123", 
    update_data={"active": False}
)
```

```
delete_alert("alert_uuid_123")
```

```
update_verified(
    doc_id="ver_uuid_456", 
    update_data={
        "status": "confirmed", 
        "confidence_score": 0.99
    }
)
```

```
delete_verified("ver_uuid_456")
```