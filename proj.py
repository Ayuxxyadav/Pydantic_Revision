import os 

from dotenv import load_dotenv

from groq import Groq
from pydantic import BaseModel ,Field

load_dotenv()
my_api_key = os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("api keys not loaded")

client = Groq(api_key= my_api_key)


class UserProfile(BaseModel):
    name:str = Field(description="Enter user full name ")
    age:str = Field(description="Enter user's age ")
    skills:list[str] = Field(description="Enter the Programming skill")
    is_employeed : bool = Field(description="Is User employeed?")


json_schema = UserProfile.model_json_schema()

chat_completion = client.chat.completions.create(
    model= "openai/gpt-oss-120b",
    temperature=0.1,
    response_format={"type":"json_object"},
    messages=[
        {
            "role":"system",
            "content":f"You are an Ai data extractor.Extract user details and return only a valid JSON object matching to this{json_schema}"
        },
        {
            "role":"user",
            "content":"I m Ayush yadav. currently i m 23 yr software dev . I code in mernstack as well as python "
        }
    ]

)

raw_response = chat_completion.choices[0].message.content
print(raw_response) # ye response bhle dikhne mai json lge but python k liye string hi h 

import json
parsed_data = json.loads(raw_response) #Isliye hum sabse pehle json.loads(raw_response) 
#likhte hain taaki wo string Python ka ek standard Dictionary (dict) ban jaye.

validate_user = UserProfile(**parsed_data) # ** isliye use kiya jata jb apko class ko pura dict key values bhejni hoti h 
#Lekin ek simple dictionary ke paas koi validation ya superpowers nahi hoti agar aapko koi galat
#  data mil jaye (jaise agar age ki jagah koi text bhej de).
#  Isi problem ko solve karne ke liye humne pehle ek Pydantic class banayi thi:
#. Ab jab hum UserProfile(parsed_data) likhte hain, toh hum Pydantic se kehte hain: 
# "Yeh lo dictionary, isko check karo aur hamare UserProfile blueprint ke hisaab se ek Pydantic Object bana kar do."

print(validate_user)
print(validate_user.skills)