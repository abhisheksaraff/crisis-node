import json
from typing import List, Dict, Any, Optional, cast
from app.schemas.alerts import AlertEntry, AlertSource, AlertAction
from app.db.news_db import get_news_locations, read_news_by_location, mark_news_read
from app.db.alerts_db import create_alert, get_alert_locations, read_alerts_by_location, add_alert_source, update_alert_action_status, mark_alert_done

class AgentService:
    # --- PHASE 1: DISCOVERY ---
    def get_agent_context(self) -> Dict[str, List[str]]:
        """Provides the agent with a high-level view of pending work."""
        return {
            "location": get_news_locations(),
            "active_alert_locations": get_alert_locations(active_only=True)
        }

    # --- PHASE 2: TRIAGE & ANALYSIS ---
    def prepare_location_data(self, location_name: str) -> Dict[str, Any]:
        """Gathers all evidence and history for a specific location."""
        return {
            "new_news": read_news_by_location(location_name),
            "existing_alerts": read_alerts_by_location(location_name, active_only=True),
            "recent_history": read_alerts_by_location(location_name, active_only=False)[:5]
        }

    # --- PHASE 3: EXECUTION ---
    # def process_new_alert(self, news_id: str, alert_data: Dict[str, Any]):
    #     """
    #     Validates output against AlertEntry schema and creates a new row.
    #     Then marks the source news as processed.
    #     """
    #     # 1. Validation check
    #     entry = AlertEntry(**alert_data)
        
    #     # 2. Save to DB (Pydantic handles UUID/Datetime serialization)
    #     result = create_alert(entry.model_dump(exclude_none=True))
        
    #     # 3. Cleanup
    #     mark_news_read(news_id)
    #     return result
    
    # def process_new_alert(self, alert_data: Dict[str, Any]):
    #     """
    #     Validates output against AlertEntry schema and creates a new row.
    #     Then marks the source news as processed.
    #     """
    #     # 1. Validation check
    #     entry = AlertEntry(**alert_data)
        
    #     # 2. Save to DB (Pydantic handles UUID/Datetime serialization)
    #     result = create_alert(entry.model_dump(exclude_none=True))
        
    #     return result
    
    def process_new_alert(self, alert_data: Dict[str, Any]):
        """
        Saves a new alert directly to the database and returns the result.
        No longer uses Pydantic for validation/serialization.
        """
        # 1. Save to DB 
        # We pass the raw dict directly; ensure types (like dates) 
        # are already stringified if necessary.
        result = create_alert(alert_data)
        
        return result

    def add_alert_source(self, alert_id: str, new_source: Dict[str, Any]):
        """
        Appends new evidence to an existing alert and cleans up news entry.
        """
        # Validate source schema
        # new_source = AlertSource(**source_data)
        
        # Add to alert
        result = add_alert_source(alert_id, new_source)
        
        # Cleanup
        #mark_news_read(news_id)
        return result

    def sync_action_status(self, alert_id: str, task_index: int, is_done: bool):
        """Standardizes action updates for the agent."""
        return update_alert_action_status(alert_id, task_index, is_done)

    def resolve_alert(self, alert_id: str):
        """Finalizes an alert once the threat has passed."""
        return mark_alert_done(alert_id)