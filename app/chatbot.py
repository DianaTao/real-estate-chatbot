import json
import openai
from input_parser import InputParserAgent
from user_profile import UserProfileAgent
from re_knowledge import REKnowledgeAgent
from property_search import PropertySearchAgent

class ButterfloChatbot:
    def __init__(self):
        openai.api_key = "YOUR_OPENAI_API_KEY"
        self.parser = InputParserAgent()
        self.user_profile_agent = UserProfileAgent({
            "name": None,
            "email": None,
            "phone_number": None
        })
        self.knowledge_agent = REKnowledgeAgent()
        self.search_agent = PropertySearchAgent(self.user_profile_agent)

    def handle_message(self, message: str) -> str:
        parsed = self.parser.parse(message)
        intent = parsed.get("intent")
        params = parsed.get("parameters", {})

        if intent == "set_profile":
            for k, v in params.items():
                setter = getattr(self.user_profile_agent, f"set_{k}", None)
                if callable(setter):
                    setter(v)
                else:
                    self.user_profile_agent.update_user_preference(k, v)
            return "User profile updated."

        if intent == "explain_term":
            return self.knowledge_agent.explain_term(params.get("term", ""))
        if intent == "answer_question":
            return self.knowledge_agent.answer_question(params.get("question", ""))
        if intent == "save_preferences":
            self.user_profile_agent.save_preferences_to_db()
            return "Your preferences have been saved."
        if intent == "search":
            try:
                return self.search_agent.run_search(params)
            except ValueError as e:
                return str(e)
        if intent == "list_saved_properties":
            sort_by = params.get("sort_by", "date_added")
            descending = params.get("descending", True)
            props = self.user_profile_agent.get_saved_properties(sort_by, descending)
            return json.dumps(props, indent=2)

        return "Sorry, I didn't understand that."

if __name__ == "__main__":
    bot = ButterfloChatbot()
    print(bot.handle_message("Search for single family homes in Denver with cap rate above 8% built after 2010"))
    print(bot.handle_message("What is ROI?"))
    print(bot.handle_message("Set profile name John Doe email john@example.com phone_number 555-1234"))
    print(bot.handle_message("Save my preferences"))
    # example
    bot.user_profile_agent.add_saved_property({"id": 1, "price": 350000, "bedrooms": 3})
    bot.user_profile_agent.add_saved_property({"id": 2, "price": 450000, "bedrooms": 4})
    print(bot.handle_message("List saved properties sorted by price descending"))