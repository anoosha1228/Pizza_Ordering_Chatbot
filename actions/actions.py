from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import UserUtteranceReverted, ActionExecuted, SessionStarted, SlotSet, Restarted, AllSlotsReset
from pymongo import MongoClient, DESCENDING
from datetime import datetime, timedelta
import csv

client = MongoClient("mongodb://localhost:27017/")
db = client["dominos_db"]

class ActionRestart(Action):

    def name(self) -> Text:
        return "action_restart"

    async def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        # Define the events to reset the conversation
        events = [
            # Revert back to the user's last message
            UserUtteranceReverted(),
            # Clear all slots
            AllSlotsReset(),
            # This is important to start a new conversation
            SessionStarted(),
            # Mark the restart action as completed
            ActionExecuted("action_restart")
        ]

        return events

        #################### pizza

class ActionFetchPizzaData(Action):
    def name(self) -> str:
        return "action_ask_pizza"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        crust = tracker.get_slot("crust")
        print(crust)

        size = tracker.get_slot("size")
        print(size)

        db_collection = db["data"]
        pizza_names = list(db_collection.find({}))

        if crust and size:

            filter_crust = []
            for item in pizza_names:
                filter_crust.append(item['Crust Type'])

            filter_crust = list(set(filter_crust))
            # print(filter_crust)

            lines_with_thin_crust = [name for name in filter_crust if crust.lower() in name]
            print(lines_with_thin_crust)

            for items in lines_with_thin_crust:
                print("item 1")
                print(items)
                pizza_filter = db_collection.find_one({"Crust Type": items, "Size": size})
                print(pizza_filter)

                if pizza_filter:
                    print(pizza_filter)
                    break
            
            if pizza_filter:
                # pizza_name = []
                # for item in pizza_names:
                #     pizza_name.append(item['Pizza Name'])
                # print("hello1")

                # pizza_name = list(set(pizza_name))

                # pizza_names_str = '\n'.join(f'- {pizza}' for pizza in pizza_name)
                pizza_list = [
                    'wisconsin 6 cheese',
                    'buffalo chicken',
                    'meatzza feast',
                    'ultimate pepperoni feast',
                    'extravaganzza feast',
                    'philly cheese steak',
                    'pacific veggie',
                    'honolulu hawaiian',
                    'cheese pizza',
                    'fiery hawaiian',
                    'spinach & feta',
                    'america\'s favorite feast',
                    'deluxe feast',
                    'bacon cheeseburger feast',
                    'memphis bbq chicken',
                    'cali chicken bacon ranch'
                ]

                pizza_names_str = '\n'.join(f'- {pizza}' for pizza in pizza_list)

                dispatcher.utter_message(text=f'What type of pizza would you like?\nChoose your flavor: \n{pizza_names_str}')
                return []
            
            else:
                events = [
                    # Revert back to the user's last message
                    UserUtteranceReverted(),
                    # Clear all slots
                    AllSlotsReset(),
                    # This is important to start a new conversation
                    SessionStarted(),
                    # Mark the restart action as completed
                    ActionExecuted("action_restart")
                ]
                dispatcher.utter_message(text=f'Sorry you choose wrong crust type for {size} pizza.\nWrite "I want pizza" And I will show you pizza list, their size and crust type.')
                return events
                
        else:
            # pizza_name = []
            # for item in pizza_names:
            #     pizza_name.append(item['Pizza Name'])
            # print("hello1")

            # pizza_name = list(set(pizza_name))

            # pizza_names_str = '\n'.join(f'- {pizza}' for pizza in pizza_name)

            pizza_list = [
                'wisconsin 6 cheese',
                'buffalo chicken',
                'meatzza feast',
                'ultimate pepperoni feast',
                'extravaganzza feast',
                'philly cheese steak',
                'pacific veggie',
                'honolulu hawaiian',
                'cheese pizza',
                'fiery hawaiian',
                'spinach & feta',
                'america\'s favorite feast',
                'deluxe feast',
                'bacon cheeseburger feast',
                'memphis bbq chicken',
                'cali chicken bacon ranch'
            ]

            pizza_names_str = '\n'.join(f'- {pizza}' for pizza in pizza_list)

            dispatcher.utter_message(text=f'What type of pizza would you like?\nChoose your flavor: \n{pizza_names_str}')
            return []

        #################### crust

class ActionFetchCrustData(Action):
    def name(self) -> str:
        return "action_ask_crust"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        pizza = tracker.get_slot("pizza")
        print(pizza)

        size = tracker.get_slot("size")
        print(size)

        db_collection = db["data"]

        if pizza and not size:
            pizza_crust = db_collection.find({"Pizza Name": pizza.lower()})

            crust = []
            for item in pizza_crust:
                print(item)
                crust.append(item['Crust Type'])
                print(crust)
            print("hello1")
            crust = list(set(crust))
            print(crust)

            components = set()
            for records in crust:
                for component in records.split(', '):
                    components.add(component)
            
            pizza_crust_str = '\n'.join(f'- {item1}' for item1 in components)

            message = f'What type of pizza crust would you like?\n{pizza_crust_str}'

        if pizza and size:
            pizza_crust = db_collection.find({"Pizza Name": pizza.lower(), "Size": size.lower()})

            crust_price_pairs = []
            for item in pizza_crust:
                print(item)
                crust_price_pairs.append((item['Crust Type'], item['Price']))
                print(crust_price_pairs)

            # Remove duplicates
            crust_price_pairs = list(set(crust_price_pairs))
            print(crust_price_pairs)

            message = f'These are the available crust types in this flavor and size.\nKindly select one:\n'

            for crust, price in crust_price_pairs:
                message += f'- {crust}, {price} dollar\n'  

        dispatcher.utter_message(text=message)
        return []

        #################### size

class ActionFetchSizeData(Action):
    def name(self) -> str:
        return "action_ask_size"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        pizza = tracker.get_slot("pizza")
        print(pizza)
        crust = tracker.get_slot("crust")
        print(crust)

        db_collection = db["data"]

        pizza_sizes = db_collection.find({"Pizza Name": pizza.lower()})

        filter_crust = []
        for item in pizza_sizes:
            print(item)
            filter_crust.append(item['Crust Type'])
            print(crust)

        filter_crust = list(set(filter_crust))
        print(filter_crust)

        lines_with_thin_crust = [name for name in filter_crust if crust.lower() in name]

        size_price_pairs = []
        for item in lines_with_thin_crust:
            pizza_sizes = db_collection.find({"Pizza Name": pizza, "Crust Type": item})
            print(pizza_sizes)
            
            for item in pizza_sizes:
                print(item)
                size_price_pairs.append((item['Size'], item['Price']))
                print(size_price_pairs)

        # Remove duplicates
        size_price_pairs = list(set(size_price_pairs))
        print(size_price_pairs)

        message = f'These are the available sizes in this flavor and crust type.\nKindly select one:\n'

        for size, price in size_price_pairs:
            message += f'- {size}, {price} dollar\n'

        dispatcher.utter_message(text=message)

        return []

                #################### price
                                        
class ActionPriceData(Action):
    def name(self) -> str:
        return "action_ask_price"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        pizza = tracker.get_slot("pizza")
        print(pizza)
        crust = tracker.get_slot("crust")
        print(crust)
        size = tracker.get_slot("size")
        print(size)

        db_collection = db["data"]

        pizza_sizes = db_collection.find({"Pizza Name": pizza.lower()})

        filter_crust = []
        for item in pizza_sizes:
            print(item)
            filter_crust.append(item['Crust Type'])
            print(crust)

        filter_crust = list(set(filter_crust))
        print(filter_crust)

        lines_with_thin_crust = [name for name in filter_crust if crust.lower() in name]

        for item in lines_with_thin_crust:
            query = {"Pizza Name": pizza, "Crust Type": item, "Size": size}
            pizza_price = db_collection.find_one(query)
            
            if pizza_price:
                print(pizza_price)
                break

        if pizza_price:
            pizza_price_ = pizza_price['Price']
            dispatcher.utter_message(text = f'Your total is {pizza_price_}')
            dispatcher.utter_message(response = 'utter_place_order')
            return [SlotSet("price", pizza_price_)]   
        else:     
            events = [
                # Revert back to the user's last message
                UserUtteranceReverted(),
                # Clear all slots
                AllSlotsReset(),
                # This is important to start a new conversation
                SessionStarted(),
                # Mark the restart action as completed
                ActionExecuted("action_restart")
            ]
            dispatcher.utter_message(text=f'Sorry you have selected wrong crust type for {size} pizza.\nWrite "I want pizza" And I will show you pizza list.')
            return events

class ActionRegister(Action):
    def name(self) -> str:
        return "action_register"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: dict) -> list:

        name = tracker.get_slot("PERSON")
        number = tracker.get_slot("phone-number")
        address = tracker.get_slot("address")
        email = tracker.get_slot("email")

        pizza = tracker.get_slot("pizza")
        crust = tracker.get_slot("crust")
        size = tracker.get_slot("size")
        price = tracker.get_slot("price")

        db_collection = db["data"]
        order_collection = db["order"]

        # def validate_name(self, value, dispatcher, tracker, domain):
        #     requested_slot = tracker.current_state()['slots']['requested_slot']
        
        #     if requested_slot == 'time':
        #         return {"time": value}
        #     else:
        #         return {"time": tracker.get_slot('time')}

        # authentication = order_collection.find_one({"name": name}, sort=[("created_date", -1)])
        # filter = {"name": name}
        # print(authentication)

        now = datetime.now()
        date_time = now.strftime("%d/%m/%Y %H:%M:%S")

        data = {
            "pizza" : pizza,
            "crust" : crust,
            "size" : size,
            "price": price
        }

        # if authentication:
        #     # order_collection.insert_one(filter, {"$set": {"items": data}})
        #     update_result = order_collection.update_one(
        #         filter,
        #         {
        #             "$push": {
        #                 "items": data
        #             }
        #         }
        #     )
        # else:
        document = {
            "name": name,
            "number": number,
            "address": address,
            "email": email,
            "items": data,
            "created_date": date_time
        }

        order_collection.insert_one(document)

        dispatcher.utter_message(f"Thank you {name} for placing order.\nYour order summary is:\nPizza: {pizza}\nCrust Type: {crust}\nSize: {size}\nTotal Price: {price}.\nYour credentials are: Address: {address}, Phone No. {number} and E-mail: {email}.")
        return[]
