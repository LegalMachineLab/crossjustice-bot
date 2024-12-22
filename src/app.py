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

from argumentation.arg_interface import get_full_theory, run_reasoner

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

    right_keys = [k for k, _ in rights.items()]

    res = prompt_model(f"""
        According to the following input, what does the user want to do?

        1. Input new facts into the system;
        2. Know which rights are deducible from her scenario;
        3. Know about one of this specific rights: {right_keys}

        Reply "1" if 1, "2" if 2, and "3 - right from the list" if 3.
        Do not include anything else in your output.

        {input_text}
    """)
    print(res)

    target = [x.strip() for x in res.split("-")][1] if "3" in res else st.session_state.target
    conformity = {}
    st.session_state.target = target
    if target and target not in st.session_state.arguments:
       print(target)
       theory = get_full_theory("\n".join([x["arg_rule"] for _, v in rights[target].items() for x in v]), ["it"])
       conformity = run_reasoner(theory)
       print(conformity)
       st.session_state.arguments[target] = conformity
    elif target:
       conformity = st.session_state.arguments[target]

    return f"""
      You must help the user to describe their case and then extract the relevant facts from this list of facts:

      {input_facts.facts + input_facts.facts_dir_2010_64}

      Make sure the user provides the following details as clearly and accurately as possible:

      Who is involved?
      - All parties must be presented explicitly.
      - If you dont know the name of the person, use anonym.
      What happened?
      - Describe the key events or conditions relevant to your case.
      - Be specific about the actions taken or situations that occurred.
      When did it happen?
      - Describe the applicable stage of the proceedings.

      Respect the following instructions:
      - DO NOT create new facts.
      - Only use the list of facts provided as input.
      - DO NOT tell the user what rights apply.
      - DO NOT ask similar questions again.

      Format of the output:
      - Include the list of Prolog facts extracted so far inside a markdown block.
      - DO NOT put comments inside the Prolog markdown block.
      - All variables must be grounded for a fact to be valid.

      These are the rights computed by the symbolic engine up to this point:

      {right_keys}

      If needed, suggest additional facts that could be relevant.
      Ask the user if they apply to the case.
      Just list the rights without additions.

    """ + (f"""
      These are the details on {target}:

      {rights[target]}

      Arguments on conformity with national implamentations [it]:

      {conformity}

      Questions on conformity can only be answered based on these arguments. Do not add anything.

    """ if target else "")

  groq_chat = ChatGroq(
      groq_api_key='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',
      model_name="llama3-70b-8192"
      #model_name="mixtral-8x7b-32768"
  )

  prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=select_prompt()),
            MessagesPlaceholder(variable_name="my_chat"),
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
      st.session_state.rights = {}
      st.session_state.chat_message = []
      st.session_state.target = ""
      st.session_state.arguments = {}
      st.session_state.memory = ConversationBufferWindowMemory(k=3, memory_key="my_chat", return_messages=True)

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
