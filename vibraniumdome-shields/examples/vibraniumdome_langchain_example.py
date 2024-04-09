#################################################################################################
# $> python -m venv venv
# $> source venv/bin/activate
# $> pip3 install vibraniumdome-sdk==0.6.0 langchain-openai
#################################################################################################

from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from vibraniumdome_sdk import VibraniumDome

VibraniumDome.init(app_name="set_you_agent_name_here")

model = ChatOpenAI(model="gpt-4", model_kwargs={
                            "extra_headers":{
                                "x-session-id": "abcd-1234-cdef"}},)
prompt = ChatPromptTemplate.from_template("tell me a short joke about {topic}")
output_parser = StrOutputParser()
chain = prompt | model | output_parser
result = chain.invoke({"topic": "ice cream"})
print(result)