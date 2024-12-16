import streamlit as st
from groq import Groq
import random

from langchain.chains import ConversationChain, LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

from swi_interface import generate_response, prettify_response
import input_facts

def prompt_model(prompt, system="", model="llama3-70b-8192", temperature=0.5):

  client = Groq(
      api_key='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',
  )

  completion = client.chat.completions.create(
      model=model,
      messages=[
          {
              "role": "system",
              "content": system
          },
          {
              "role": "user",
              "content": prompt
          }
      ],
      temperature=temperature,
      top_p=1,
      stream=True,
      stop=None,
  )

  return "".join([chunk.choices[0].delta.content or "" for chunk in completion])


person_id = "anonym"

def parse_output(user_text):

  def extract_code(completion):
    from mdextractor import extract_md_blocks
    blocks = extract_md_blocks(completion)
    return blocks[0] if blocks else ""

  user_facts = [x for x in extract_code(user_text).replace(".", "").split("\n") if x]
  #if user_facts:
    #personId = "anonym"
    #personId = prompt(f"Extract the personId from this list of facts: {user_facts}.")

  return user_text, user_facts

def llm_response(input_text, person_id, user_facts, rights, memory):

  def select_prompt():

    res = prompt_model(f"According to the following input, does the user want to know her rights?\nReply OUTPUT if that is the case.\n\n{input_text}")
    print(res)

    return f"""
        You must help the user to describe their case and then extract the relevant facts from this list of facts:

        {input_facts.facts + input_facts.facts_dir_2016_800}

        Make sure that all the facts are extracted correctly!
        Do not create new facts!

        Include a list of Prolog facts extracted so far inside a markdown block.

        Suggest to the user facts that could be relevant but he didnt mention.

        Do not put textual comments inside the Prolog markdown block.
        All variables must be grounded for a fact to be valid.
        If you dont know the value of PersonId, use anonym.
      """ if "INPUT" in res or not rights else f"""

        These are the rights computed by the symbolic engine til now:

        {rights[0]}

        Make the user know them.
      """

  groq_chat = ChatGroq(
      groq_api_key='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',
      model_name="llama3-70b-8192"
      #model_name="mixtral-8x7b-32768"
  )

  prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=select_prompt()),
            MessagesPlaceholder(variable_name="chat_message"),
            HumanMessagePromptTemplate.from_template("{human_input}")
        ])

  conversation = LLMChain(
      llm=groq_chat,
      prompt=prompt,
      verbose=False,
      memory=memory,
  )

  return conversation.predict(human_input=input_text)

def main():

    st.title("Chat with CrossJustice!")

    if "chat_message" not in st.session_state:
      st.session_state.facts = []
      st.session_state.rights = []
      st.session_state.chat_message = []
      st.session_state.memory = ConversationBufferWindowMemory(k=10, memory_key="chat_message", return_messages=True)

    for message in st.session_state.chat_message:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_question := st.chat_input("Describe your case:"):

        with st.chat_message("user"):
          st.markdown(user_question)

        st.session_state.chat_message.append({"role": "user", "content": user_question})

        response = llm_response(user_question, person_id, st.session_state.facts, st.session_state.rights, st.session_state.memory)

        try:
          txt, user_facts = parse_output(response)
          if user_facts:
            facts, prolog_response = generate_response(person_id, user_facts, ["dir"])
            pretty = prettify_response(prolog_response, facts)
            st.session_state.rights = pretty
            st.session_state.facts = user_facts
            print(facts)
            print(pretty)
        except Exception as e:
          print(e)

        with st.chat_message("ai"):
          st.markdown(response)

        st.session_state.chat_message.append({"role": "ai", "content": response})

if __name__ == "__main__":
    main()
