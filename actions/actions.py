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
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

import json, os

class ActionBookFlight(Action):
    def name(self) -> Text:
        return "action_book_flight"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        departure_city = tracker.get_slot("departure_city")
        arrival_city = tracker.get_slot("arrival_city")
        travel_date = tracker.get_slot("travel_date")

        flight = {
            "departure_city": departure_city,
            "arrival_city": arrival_city,
            "travel_date": travel_date,
            "id": 0
        }

        if os.path.exists("flightLog.txt"):
            with open("flightLog.txt", "r") as file:
                lines = file.readlines()
                if lines:
                    last_flight = json.loads(lines[-1])
                    flight["id"] = last_flight["id"] + 1

        
        with open("flightLog.txt", "a") as file:
            file.write(json.dumps(flight) + "\n")

        dispatcher.utter_message(
            text=f"Booking flight from {departure_city} to {arrival_city} on {travel_date}."
        )


        return [
            SlotSet("departure_city", None),
            SlotSet("arrival_city", None),
            SlotSet("travel_date", None)
        ]
    
class ActionLookupFlightLog(Action):
    def name(self) -> Text:
        return "action_lookup_flight_log"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if not os.path.exists("flightLog.txt"):
            dispatcher.utter_message(text="No flight log found.")
            return []
        
        with open("flightLog.txt", "r") as file:
            lines = file.readlines()
        
        if not lines:
            dispatcher.utter_message(text="No flights have been booked yet.")
            return []
        
        flight_logs = [json.loads(line) for line in lines]
        flight_details = "\n".join(
            f"Flight ID: {flight['id']}, From: {flight['departure_city']}, To: {flight['arrival_city']}, Date: {flight['travel_date']}"
            for flight in flight_logs
        )
        
        dispatcher.utter_message(
            text=f"Here are the booked flights:\n{flight_details}"
        )
        
        return []
    
class ActionCancelFlight(Action):
    def name(self) -> Text:
        return "action_cancel_flight"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        flight_id = tracker.get_slot("flight_id")

        
        flight_id = int(flight_id)
        
        if not os.path.exists("flightLog.txt"):
            dispatcher.utter_message(text="No flight log found.")
            return []

        with open("flightLog.txt", "r") as file:
            lines = file.readlines()
        
        flight_logs = [json.loads(line) for line in lines]
        flight_to_remove = next((flight for flight in flight_logs if flight["id"] == flight_id), None)
        
        if not flight_to_remove:
            dispatcher.utter_message(text=f"No flight found with ID {flight_id}.")
            return []

        flight_logs.remove(flight_to_remove)
        
        with open("flightLog.txt", "w") as file:
            for flight in flight_logs:
                file.write(json.dumps(flight) + "\n")
        
        dispatcher.utter_message(text=f"Flight ID {flight_id} has been removed from the log.")
        
        return [SlotSet("flight_id", None)]

class ActionResetLog(Action):
    def name(self) -> Text:
        return "action_reset_log"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        if os.path.exists("flightLog.txt"):
            os.remove("flightLog.txt")
        
        dispatcher.utter_message(text="Flight log has been reset.")
        
        return []