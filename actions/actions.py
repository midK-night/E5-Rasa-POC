# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

class ActionBookFlight(Action):
    def name(self) -> Text:
        return "action_book_flight"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # departure_city = tracker.get_slot("departure_city")
        # arrival_city = tracker.get_slot("arrival_city")
        # travel_date = tracker.get_slot("travel_date")

        # print("DEBUG: action_submit_flight called") 
        # print(f"DEBUG: Slots - From: {departure_city}, To: {arrival_city}, Date: {travel_date}")

        # dispatcher.utter_message(
        #     text=f"Booking flight from {departure_city} to {arrival_city} on {travel_date}."
        # )

        dispatcher.utter_message(text="🎉 This works!")


        return []