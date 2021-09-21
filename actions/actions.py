# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from main import sendrandom
from typing import Any, Text, Dict, List
import rasa.core.tracker_store
from rasa_sdk.events import SlotSet,UserUtteranceReverted,EventType, Restarted
from rasa.shared.core.trackers import DialogueStateTracker
from rasa_sdk import Action, Tracker,FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
import sqlite3
import time
# import main

class ActionGetChatStartTime(Action):
    def name(self) -> Text:
        return "action_get_start_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            start_time=time.time()
           
            
            return [SlotSet("start_time", start_time)]


class ActionGetChatEndTime(Action):
    def name(self) -> Text:
        return "action_get_end_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
             
            end_time=time.time()

            return [SlotSet("end_time", end_time)]

class ActionGetUniqueId(Action):
    def name(self) -> Text:
        return "action_get_unique_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
           
            randomstring=sendrandom()
            # print("hello")
            print("Unique number in actions.py is: ",randomstring)

            return [SlotSet("unique_id", randomstring)]
        
# def sendrandomnumber(randomstring):
#     return randomstring



class ActionSaveFeedback(Action):

    def name(self) -> Text:
        return "action_save_feedback"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            try:
                db=sqlite3.connect("./details.db")
                cursor=db.cursor()
                chat_start_time=tracker.get_slot("start_time")
                chat_end_time=tracker.get_slot("end_time")
                Rating1=tracker.get_slot("realistic")
                Rating2=tracker.get_slot("robotic")
                Rating3=tracker.get_slot("welcoming")
                Rating4=tracker.get_slot("unfriendly")
                Rating5=tracker.get_slot("explainedscope")
                Rating6=tracker.get_slot("indication")
                Rating7=tracker.get_slot("navigate")
                Rating8=tracker.get_slot("confused")
                Rating9=tracker.get_slot("understoodme")
                Rating10=tracker.get_slot("recogniseinputs")
                Rating11=tracker.get_slot("appropriateresponses")
                Rating12=tracker.get_slot("irrelevant")
                Rating13=tracker.get_slot("copeerrors")
                Rating14=tracker.get_slot("unablehandle")
                Rating15=tracker.get_slot("easytouse")
                Rating16=tracker.get_slot("complex")
                sender_id=tracker.current_state()['sender_id']
                q="UPDATE UserDetails SET Realistic= ?,Robotic= ?,Welcoming= ?,Unfriendly= ?,ExplainedScope= ?,Indication= ?, Navigate= ?,Confused= ?,Understoodme=?, RecogniseInputs= ?, AppropriateResponses= ?, Irrelevant= ?, CopeErrors= ?, UnableHandle= ?, EasytoUse= ?, Complex= ?, StartTime= ?, EndTime=? WHERE UserID = ?",(Rating1,Rating2,Rating3,Rating4,Rating5,Rating6,Rating7,Rating8,Rating9,Rating10,Rating11,Rating12,Rating13,Rating14,Rating15,Rating16,sender_id, chat_start_time, chat_end_time)
                result=cursor.execute(q)
                if result==0:
                    print("Couldn't find such a database")
                else:
                    print("Ratings from user Saved Successfully!!")
            # DataUpdate(tracker.get_slot("name"),tracker.get_slot("age"),tracker.get_slot("country"))
                    # dispatcher.utter_message(response="utter_details_thanks")
            except Exception as e:
                print(str(e))
                dispatcher.utter_message(text="Something went wrong! Rating not saved to DB")
            finally:
                cursor.close()
                db.close()

        # dispatcher.utter_message(text="Hello World!")
            
            return []


class ActionRestart(Action):

    def name(self) -> Text:
        return "action_restart"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            
            return [Restarted()]




class ActionSayName(Action):

    def name(self) -> Text:
        return "action_say_name"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        Name = tracker.get_slot("name")
        if not Name:
            dispatcher.utter_message(text="I don't know your name.")
        else:
            dispatcher.utter_message(text="I have a very good memory!. Your name is {Name} ! ")
        return []

class BotEvaluationForm(Action):

    def name(self) -> Text:
        return "bot_evaluation_form"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            required_slots=["appropriateresponses","complex","confused","copeerrors","easytouse","explainedscope","indication","irrelevant","realistic","navigate","recogniseinputs","robotic","unablehandle","understoodme","unfriendly","welcoming"]
            for slot_name in required_slots:
                if tracker.slots.get(slot_name) is  None:
                    return [SlotSet("requested_slot",slot_name)]

                return [SlotSet("requested_slot",None)]

# class UserDetailsForm(Action):

#     def name(self) -> Text:
#         return "user_details_form"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#             required_slots=["name","age","country"]
#             for slot_name in required_slots:
#                 if tracker.slots.get(slot_name) is  None:
#                     return [SlotSet("requested_slot",slot_name)]

#             return [SlotSet("requested_slot",None)]


class ActionSubmit(Action):
    def name(self)->Text:
        return "action_submit"
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            try:
                db=sqlite3.connect("details.db")
                
                cursor=db.cursor()
                sender_id=tracker.current_state()['sender_id']
                Name=tracker.get_slot("name")
                # Age=tracker.get_slot("age")
                # Country=tracker.get_slot("country")
                unique_id=tracker.get_slot("unique_id")
                chat_start_time=0
                chat_end_time=0
                Rating1=0
                Rating2=0
                Rating3=0
                Rating4=0
                Rating5=0
                Rating6=0
                Rating7=0
                Rating8=0
                Rating9=0
                Rating10=0
                Rating11=0
                Rating12=0
                Rating13=0
                Rating14=0
                Rating15=0
                Rating16=0
                # q="""INSERT INTO UserDetails VALUES(?,?,?,?,?);"""
                result=cursor.execute("INSERT INTO UserDetails VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",(sender_id,unique_id,Name,Rating1,Rating2,Rating3,Rating4,Rating5,Rating6,Rating7,Rating8,Rating9,Rating10,Rating11,Rating12,Rating13,Rating14,Rating15,Rating16,chat_start_time,chat_end_time))
                if result==0:
                    print("Couldn't find such a database")
                else:
            # DataUpdate(tracker.get_slot("name"),tracker.get_slot("age"),tracker.get_slot("country"))
                    dispatcher.utter_message(response="utter_details_thanks")
                    db.commit()
                    db.close()
            except Exception as e:
                print(str(e))
                dispatcher.utter_message(text="Something went wrong! Data not saved to DB")
            # dispatcher.utter_message(response="utter_details_thanks")
            finally:
                db.close()



# class ValidateDetailsForm(FormValidationAction):
#     def name(self) -> Text:
#         return "validate_user_details_form"

#     def validate_name(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: "DomainDict") -> Dict[Text, Any]:  
#         print("################# name validation running #############################")
#         # If the name is super short, it might be wrong.
#         print(f"Name given = {slot_value} length = {len(slot_value)}")
#         if isinstance(slot_value, int)== True:
#             dispatcher.utter_message(text="I think you are kidding!")
#             return {"name": None}
#         else:
#             if len(slot_value) <= 2:
#                 dispatcher.utter_message(response="utter_name_short")
#                 return {"name": None} 
#             else:
#                 print("Name correctly filled in to slot")
#                 return {"name": slot_value}


#     def validate_age(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: "DomainDict",
#     ) -> Dict[Text, Any]:
#         """Validate `age` value."""
#         print("################# age validation running #############################")
#         # If the age is super short, it might be wrong.
#         print(f"Age given = {slot_value} length = {len(slot_value)}")
#         if isinstance(int(slot_value), int)== True:     
#             if int(slot_value) <= 0:
#                 dispatcher.utter_message(response="utter_not_born")
#                 return {"age": None}
#             else:
#                 if int(slot_value) >100:
#                     dispatcher.utter_message(text="Really!! That's too much!!")
#                     return {"age": None}
#                 elif int(slot_value) >60:
#                     dispatcher.utter_message(text="Hey! Com'on! Age is just a number. You seem to be just 20! ❤️")
#                     return {"age": slot_value}
#                 elif int(slot_value) >= 40 & int(slot_value)<=50:
#                     dispatcher.utter_message(text="Oh! You are young 😎")
#                     return {"age": slot_value}
#                 elif int(slot_value) < 40 & int(slot_value)>=20:
#                     dispatcher.utter_message(text="That's sweet 🥰")
#                     return {"age": slot_value}
#                 else:
#                     dispatcher.utter_message(text="Cool!!")
#                     return {"age": slot_value}
#         else:
#             dispatcher.utter_message(text="I think you are kidding. Really appreciate if you could share your age")
#             return {"age": None}


#     def validate_country(
#         self,
#         slot_value: Any,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: "DomainDict",
#     ) -> Dict[Text, Any]:
#         """Validate `country` value."""
#         print("################# country validation running #############################")
#         print(f"Country name given = {slot_value} length = {len(slot_value)}")
#         # c={slot_value}
#         # if isinstance(int(slot_value), int)== True:
#         #     dispatcher.utter_message(text="I think you are kidding!")
#         #     return {"country": None}
#         # else:    
#         # If the name is super short, it might be wrong.
#         if slot_value.lower() in c_list:
#             print("Country correctly filled in to slot")
#             return {"country": slot_value}
            
#         else:
#             dispatcher.utter_message(response="utter_wrong_country")
#             return {"country": None}
            
    

# ,Name=tracker.get_slot("name"),Age=tracker.get_slot("age"),Country=tracker.get_slot("country")



# class ActionGreet(Action):

#     def name(self) -> Text:
#         return "action_greet"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hey!!")

#         return [UserUtteranceReverted()]



# class ActionReceiveName(Action):

#     def name(self) -> Text:
#         return "action_receive_name"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         text = tracker.latest_message['text']
#         # dispatcher.utter_message(text=f"I'll remember your name {text}!")
#         return [SlotSet("name", text)]


# class ActionSayName(Action):

#     def name(self) -> Text:
#         return "action_say_name"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         name = tracker.get_slot("name")
#         if not name:
#             dispatcher.utter_message(text="I don't know your name.")
#         else:
#             dispatcher.utter_message(text=f"Your name is {name}!")
#         return []

# class ActionReceiveAge(Action):

#     def name(self) -> Text:
#         return "action_receive_age"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         text = tracker.latest_message['text']
#         if text>60:
#             dispatcher.utter_message(text=f"Hey! Com'on! Age is just a number. You seem to be just 20! ❤️")
#         elif text>=40 & text<=30:
#             dispatcher.utter_message(text=f"Oh! You are young 😎")
#         elif text<40 & text>=20:
#             dispatcher.utter_message(text=f"That's sweet 🥰")
#         else:
#             dispatcher.utter_message(text=f"Cool!!")
#         return [SlotSet("age", text)]


# class ActionReceiveCountry(Action):

#     def name(self) -> Text:
#         return "action_receive_country"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         text = tracker.latest_message['text']
#         dispatcher.utter_message(text=f"Thank you for your response! I will not bother you again with any personal questions. Trust me! 😄")
#         return [SlotSet("country", text)]





# country_list=["Afghanistan","Albania","Algeria","American Samoa","Andorra","Angola","Anguilla","Antarctica","Antigua and Barbuda","Argentina","Armenia","Aruba","Australia","Austria","Azerbaijan","Bahamas","Bahrain","Bangladesh","Barbados","Belarus","Belgium","Belize","Benin","Bermuda","Bhutan","Bolivia","Bosnia and Herzegovina","Botswana","Bouvet Island","Brazil","British Indian Ocean Territory","Brunei Darussalam","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Canada","Cape Verde","Cayman Islands","Central African Republic","Chad","Chile","China","Christmas Island","Cocos","Keeling Islands","Colombia","Comoros","Congo","Cook Islands","Costa Rica","Cote D'Ivoire","Ivory Coast","Croatia","Hrvatska","Cuba","Cyprus","Czech Republic","Denmark","Djibouti","Dominica","Dominican Republic","East Timor","Ecuador","Egypt","El Salvador","Equatorial Guinea","Eritrea","Estonia","Ethiopia","Falkland Islands","Malvinas","Faroe Islands","Fiji","Finland","France","France","Metropolitan","French Guiana","French Polynesia","French Southern Territories","Gabon","Gambia","Georgia","Germany","Ghana","Gibraltar","Greece","Greenland","Grenada","Guadeloupe","Guam","Guatemala","Guinea","Guinea-Bissau","Guyana","Haiti","Heard and McDonald Islands","Honduras","Hong Kong","Hungary","Iceland","India","Indonesia","Iran","Iraq","Ireland","Israel","Italy","Jamaica","Japan","Jordan","Kazakhstan","Kenya","Kiribati","Korea","North","Korea","South","Kuwait","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Libya","Liechtenstein","Lithuania","Luxembourg","Macau","Macedonia","Madagascar","Malawi","Malaysia","Maldives","Mali","Malta","Marshall Islands","Martinique","Mauritania","Mauritius","Mayotte","Mexico","Micronesia","Moldova","Monaco","Mongolia","Montserrat","Morocco","Mozambique","Myanmar","Namibia","Nauru","Nepal","Netherlands","Netherlands Antilles","New Caledonia","New Zealand","Nicaragua","Niger","Nigeria","Niue","Norfolk Island","Northern Mariana Islands","Norway","Oman","Pakistan","Palau","Panama","Papua New Guinea","Paraguay","Peru","Philippines","Pitcairn","Poland","Portugal","Puerto Rico","Qatar","Reunion","Romania","Russian Federation","Rwanda","Saint Kitts and Nevis","Saint Lucia","Saint Vincent and The Grenadines","Samoa","San Marino","Sao Tome and Principe","Saudi Arabia","Senegal","Seychelles","Sierra Leone","Singapore","Slovak Republic","Slovenia","Solomon Islands","Somalia","South Africa","S. Georgia and S. Sandwich Isls.","Spain","Sri Lanka","St. Helena","St. Pierre and Miquelon","Sudan","Suriname","Svalbard and Jan Mayen Islands","Swaziland","Sweden","Switzerland","Syria","Taiwan","Tajikistan","Tanzania","Thailand","Togo","Tokelau","Tonga","Trinidad and Tobago","Tunisia","Turkey","Turkmenistan","Turks and Caicos Islands","Tuvalu","Uganda","Ukraine","United Arab Emirates","UAE","United Kingdom","Britain","UK","United States of America","USA","US Minor Outlying Islands","Uruguay","Uzbekistan","Vanuatu","Vatican City State","Holy See","Venezuela","Viet Nam","Virgin Islands","British","Virgin Islands","US","Wallis and Futuna Islands","Western Sahara","Yemen","Yugoslavia","Zaire","Zambia","Zimbabwe"]
# c_list=[]
# for item in country_list:
#     c_list.append(item.lower())
# print(c_list)

# c="Sweden"
# if c.lower() in c_list:
#     print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^I'm found^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")

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

# class ActionSaveConversation(Action):

#     def name(self) -> Text:
#         return "action_save"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#         f = open("output.txt", "a")
#         print("**************************file opened***********************************")
#         datalist=tracker.events
        
#         for i in datalist:
#             if i['name']=="action_session_start":
#                 print("--------New conversation started-----------",tracker.current_state()['sender_id'])
#                 f.write(tracker.current_state()['sender_id'])
#             if i['event']=="user":
#                 print('user: ',i['parse_data']['text'])
#                 f.write('user: {}'.format(i['text']))
#             elif i['event']=="bot":
#                 print('bot: ',i['parse_data']['text'])
#                 f.write('bot: {}'.format(i['text']))
#         #dispatcher.utter_message(text="Data saved!")
#         print("Data Saved Successfully")
#         f.close()
#         return []
