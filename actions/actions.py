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
from typing import Any, Text, Dict,List
from urllib import response
import re

import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import csv
from pyparsing import Regex

from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.events import AllSlotsReset
from rasa_sdk.executor import CollectingDispatcher

class ActionComplain(Action):

    def __init__(self):
        self.faq_data = pd.read_csv('data/faq_data_ina.csv')
    
    def name(self) -> Text:
        return "action_act_complain"#

    def run(self, dispatcher:CollectingDispatcher, tracker:Tracker, domain):
        


        nik_slot = tracker.get_slot('nik')
        name_slot = tracker.get_slot('name')
        mail_slot = tracker.get_slot('mail')
        complain = tracker.get_slot('complain')
        questions = self.faq_data['question'].values.tolist()
        
        with open('forms.csv','a',newline='') as form:
            fieldnames = ['nik','name','mail','complain']
            csv_writer = csv.DictWriter(form, fieldnames=fieldnames)
            #csv_writer.writeheader()
            csv_writer.writerow({'nik':nik_slot,'name':name_slot,'mail':mail_slot,'complain':complain})

        print("Complain: ", complain)

        mathed_question, score = process.extractOne(complain, questions,scorer = fuzz.token_set_ratio)
        
        print('mathed queston ', mathed_question)
        print('score', score)
        if score > 50:
            matched_row = self.faq_data.loc[self.faq_data['question'] == mathed_question]
            answer = matched_row['answer'].values[0]

            response = answer
        else:
            response = "Maaf, kami tidak bisa membantu anda"

        dispatcher.utter_message(response)

        return [AllSlotsReset()]

class ValidateCustomerForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_customer_form"
        

    def validate_nik(
        self,
        slot_value: Any,
        dispatcher:CollectingDispatcher,
        tracker: Tracker,
        domain
    ) -> Dict[Text, Any]:
    
        if len(slot_value) <16:
            dispatcher.utter_message(text=f"Tolong masukkan nik anda dengan benar!")
            return {"nik": None}
        else:
            return {"nik": slot_value}

    def validate_name(
        self,
        slot_value: Any,
        dispatcher:CollectingDispatcher,
        tracker: Tracker,
        domain
    ) -> Dict[Text, Any]:
    
        if len(slot_value) < 1 :
            dispatcher.utter_message(text=f"Tolong masukkan nama anda dengan benar!")
            return {"name": None}
        else:
            return {"name": slot_value}

    def validate_mail(
        self,
        slot_value: Any,
        dispatcher:CollectingDispatcher,
        tracker: Tracker,
        domain
    ) -> Dict[Text, Any]:
        regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
    
        if (re.fullmatch(regex, slot_value)):
            
            return {"mail": slot_value}
        else:
            dispatcher.utter_message(text=f"Tolong masukkan E-mail anda dengan benar!")
            return {"mail": None}


    def validate_complain(
        self,
        slot_value: Any,
        dispatcher:CollectingDispatcher,
        tracker: Tracker,
        domain
    ) -> Dict[Text, Any]:
    
        if len(slot_value) <1:
            dispatcher.utter_message(text=f"Tolong masukkan masalah anda dengan benar!")
            return {"complain": None}
        else:
            return {"complain": slot_value}








    
