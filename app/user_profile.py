import json
from typing import Optional, Any, Dict, List

class UserProfileAgent:
    def __init__(self, user_profile: Optional[Dict[str, Any]] = None):
        self.user_profile = user_profile or {
            "name": None,
            "email": None,
            "phone_number": None
        }
        self.saved_properties: List[Dict[str, Any]] = []

    def set_name(self, name: str):
        self.user_profile["name"] = name

    def set_email(self, email: str):
        self.user_profile["email"] = email

    def set_phone_number(self, phone: str):
        self.user_profile["phone_number"] = phone

    def get_user_default(self, key: str) -> Optional[Any]:
        return self.user_profile.get(key)

    def update_user_preference(self, key: str, value: Any):
        self.user_profile[key] = value

    def save_preferences_to_db(self):
        print("Saving user profile to DB:", json.dumps(self.user_profile, indent=2))

    def add_saved_property(self, property_data: Dict[str, Any]):
        """Add a property dict to saved properties."""
        property_data["date_added"] = property_data.get("date_added") or __import__('datetime').datetime.utcnow().isoformat()
        self.saved_properties.append(property_data)

    def get_saved_properties(self, sort_by: str = "date_added", descending: bool = True) -> List[Dict[str, Any]]:
        """Return saved properties sorted by a given key."""
        # Validate sort key
        if not self.saved_properties or sort_by not in self.saved_properties[0]:
            return self.saved_properties
        return sorted(
            self.saved_properties,
            key=lambda x: x.get(sort_by),
            reverse=descending
        )

    def clear_saved_properties(self):
        """Remove all saved properties."""
        self.saved_properties.clear()

    def to_json(self) -> Dict[str, Any]:
        return {
            **self.user_profile,
            "saved_properties": self.saved_properties
        }
