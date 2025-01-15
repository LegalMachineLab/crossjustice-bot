import re
import streamlit as st
from groq import Groq
import time

from langchain.chains import LLMChain
from langchain_core.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain_core.messages import SystemMessage
from langchain.chains.conversation.memory import ConversationBufferWindowMemory, ConversationSummaryBufferMemory
from langchain_groq import ChatGroq

import input_facts
from swi_interface import query
from argumentation.arg_interface import get_full_theory, run_reasoner


def prompt_model(prompt, system="", model="llama3-70b-8192", temperature=0.3):
  client = Groq(
      api_key='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',
  )

  while True:
    try:
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
    except Exception as e:
      time.sleep(3)


def arg_hash(context):
  return hash(f"{context["right_target"]} - {context["country_target"]} - {context["opt_target"]} - {context["facts"]}")


def pretty_rights(context):
   return [i["article"] + " - " + i["right"] + " - " + i["option"] for _, v in context["rights"].items() for i in v["directive"]]


def filter_target(rights, context):
   if context["right_target"] not in rights:
      return {}
   return {k : [i for i in v if i["option"] == context["opt_target"]] for k, v in rights[context["right_target"]].items()}


def filter_target_inverse(rights, context):
   if context["right_target"] not in rights:
      return {}
   return {k : [i for i in v if i["option"] != context["opt_target"]] for k, v in rights[context["right_target"]].items()}


def select_prompt(context):

    return f"""
      Follow all instructions of Phase 1, before Phase 2.

      Phase 1: Interacting with the user.
      Assist the user in building a comprehensive case description by extracting relevant Prolog facts, while conversing with the user.
      There are certain facts which are essential and must always apply, unless explicitly stated otherwise: '''{input_facts.facts}'''.

      Consider also if any of the following conditions may be relevant :'''{input_facts.dir_facts[context["directive_target"]]} {input_facts.national_facts[context["directive_target"]][context["country_target"]]}'''.
      Evaluate whether these facts can reasonably apply to the given scenario.
      You can extract all facts that are present, if similar or equivalent facts apply.
      Avoid asking yes or no questions. Just ask a few questions on the state of the scenario.

      Respect the following instructions:
      - DO NOT create new facts.
      - DO NOT tell the user what rights may apply.
      - DO NOT ask similar questions more than once.

      Format of the output:
      - INCLUDE THE LIST OF PROLOG FACTS EXTRACTED inside a single markdown block.
      - DO NOT create more than one block. Keep all facts in a single one.
      - DO NOT put comments inside the markdown block.
      - All variables must be lower letter for a fact to be valid.

      These are the facts the user provided so far:

      {context["facts"]}

      After some questions ask the users if they wants to know what rights they have.

    """ + (f"""
      Phase 2: Presenting the rights computed by the symbolic engine.

      Rights granted at the European level:

      {"\n".join(pretty_rights(context))}

      Respect this instruction:
      DO NOT invent any rights, only present what has been computed.

      Format of the answer:
      Tell the user the list of computed rights in natural language.
      If no rights apply, ask the user if more details should be provided to the scenario.

      If rights are granted, ask if the user wants to know more details any of these rights.

    """ if context["state"] == "2" else "") + (f"""

      Phase 3: Explaining the Rights

      These are the details on {context["right_target"]} - {context["opt_target"]}:

      {filter_target(context["rights"], context)}

      Respect this instruction:
      DO NOT invent any rights, only present what has been computed.

      The right has a label, a corresponding article, and an option (specific application).
      One right can have multiple options. Show all the options.

      RESPECT this format to explain the right:
      - Explain what each right refers to.
      - Tell the user the article and source of origin.
      - Give a summary of the conditions for the application of the specific right.

      Ask if the user wants to know about the conformity evaluation with the European country about any right.
      Questions on conformity can only be answered based on the following text. Do not add anything.

      {context["pretty_arguments"][arg_hash(context)]}

      Following is the list of rights for different options in the national implementation:

      {filter_target_inverse(context["target"], context)}

      If there is no list, tell the user no rights are granted in the specific EU state.
      If there are rights, tell the user the list of national rights in natural language.

      These are specific and additional facts required by the national implementation: '''{context["suggestions"]}'''.
      If there are no facts, tell the user such.
      If there's more than one fact, tell the user some facts may be needed for the national law to apply in this specific scenario.
      Provide the user a brief explanation of these facts in natural language.

    """ if context["right_target"] and arg_hash(context) in context["pretty_arguments"] else "")


def select_state(messages, context):
    res = prompt_model(f"""
        According to the following input, what does the user want to do?

        1. Input new facts into the system;
        2. Know which rights are deducible from her scenario;
        3. Know about one of this specific rights: {pretty_rights(context)}

        Reply "1" if 1, "2" if 2, and "3 - article - right - option (from the list)" if 3.
        Do not include anything else in your output.

        {messages[-2:]}
    """)

    print("Selecting State:")
    print(res)
    print()

    context["right_target"] = [x.strip() for x in res.split("-")][2] if "3" in res else context["right_target"]
    context["opt_target"] = [x.strip() for x in res.split("-")][3] if "3" in res else context["opt_target"]
    raw_state = [x.strip() for x in res.split("-")][0]
    context["state"] = "1" if "1" in raw_state else "2" if "2" in raw_state else "3"


def run_argumentation(context):
    if context["right_target"] and context["country_target"] and arg_hash(context) not in context["arguments"]:
      rules = [x["arg_rule"] for _, v in filter_target(context["rights"], context).items() for x in v] + [x["arg_rule"] for _, v in filter_target(context["target"], context).items() for x in v]
      theory = get_full_theory("\n".join(rules), [context["country_target"]])
      context["arguments"][arg_hash(context)] = run_reasoner(theory)
      context["pretty_arguments"][arg_hash(context)] = prompt_model(f"""
        Arguments on conformity with national implementations [{context["country_target"]}]:

        {context["arguments"][arg_hash(context)]}

        Arguments are either IN or OUT:
         - If IN they are accepted according to Dung's grounded semantics;
         - If OUT they are rejected according to Dung's grounded semantics;

        To extract the conformity analyze the IN arguments provided, ignore the OUT arguments.
        Read the IN arguments to define the level of conformity.
        There are three levels of conformity:
          - if you read in the IN arguments ((conformity(COUNTRY, ART)) it means there is Full Conformity: All rights and conditions are identical between EU and national implementation.
          - if you read in the IN arguments ('-'(conformity(COUNTRY, ART)) it means there is No Conformity: No rights are granted under the national implementation.
          - if you read in the IN arguments (partial_conformity(COUNTRY, ART)) it means there is Partial Conformity: Rights are granted, but under different conditions than the european source.

        If there's full conformity, tell the user the right is granted.
        If there's no conformity, tell the user the right is not granted under national law.
        If there's partial conformity, evaluate the conditions required by the national implementation of the EU and National rights.
        Analyze the key differences between the two. Focus on the meaning of the relevant facts.

        Details on national implementation:

        {filter_target(context["target"], context)}

        Details on european implementation:

        {filter_target(context["rights"], context)}

        Explain if there is conformity and why.
      """)
      print("Argumentation result:")
      print(context["arguments"][arg_hash(context)])
      print()
      print("Argumentation parsed:")
      print(context["pretty_arguments"][arg_hash(context)])
      print()


def parse_output(user_text):
  def _extract_code(completion):
    from mdextractor import extract_md_blocks
    blocks = extract_md_blocks(completion)
    return blocks[0] if blocks else ""

  return [x for x in [y.strip().split("%")[0] for y in _extract_code(user_text).replace(".", "").split("\n")] if x]


def run_dir_prolog(output, context):
  try:
    user_facts = parse_output(output)
    if user_facts:
      context["person_id"] = re.search(r"person_status\((.+),", "\n".join(user_facts)).group(1).strip()
      response = query(context["person_id"], user_facts, ["dir"], [context["directive_target"]])
      context["facts"] = user_facts
      context["rights"] = response
      print("Dir rights:")
      print(context["person_id"])
      print(context["facts"])
      print(context["rights"])
      print()
  except Exception as e:
    print(e)


def run_national_prolog(context):
  try:
    response = query(context["person_id"], context["facts"], [context["country_target"]], [context["directive_target"]], right=context["right_target"]) # opt=context["opt_target"]
    context["target"] = response
    print("National result:")
    print(context["target"])
    print()
  except Exception as e:
    print(e)


def suggest_facts(context):
  if not context["country_target"] or not context["right_target"] or not context["person_id"]:
     return
  try:
      response = query(context["person_id"], context["facts"], [context["country_target"]], [context["directive_target"]], right=context["right_target"], abduce=True) # opt=context["opt_target"]
      abduced = set([y for _, v in response[context["right_target"]].items() for x in v for y in x["abduced"]])
      context["suggestions"] = abduced
      print("Abduction result:")
      print(context["suggestions"])
      print()
  except Exception as e:
    print(e)


def llm_response(input_text, context, memory):
  return LLMChain(
      llm=memory.llm,
      prompt=ChatPromptTemplate.from_messages(
        [
            SystemMessage(content=select_prompt(context)),
            MessagesPlaceholder(variable_name="my_chat"),
            HumanMessagePromptTemplate.from_template("{human_input}")
        ]),
      verbose=False,
      memory=memory,
  ).predict(human_input=input_text)


def main():

    #st.title("Chat with CrossJustice!")

    dirs = ["directive_2010_64", "directive_2012_13", "directive_2016_343", "directive_2013_48"]
    selected_dir = st.sidebar.selectbox('Choose from the list the relevant directives: Directive 2010/64 on right to interpretation and translation; 2012/13 on the right to information, 2016/343 on the presumption of innocence; 2013/48 on the right of access to a lawyer', dirs)

    laws = ["it", "nl", "bg", "pl"]
    selected_law = st.sidebar.selectbox('Choose the country where the proceedings are taking place, therefore the applicable national law:', laws)

    st.sidebar.markdown("""
      ## Welcome to the Tutorial

      This is a simple tutorial on how to use the bot.

      ### Select dir and law:
      1. Select an option from the dropdown in the sidebar.
      2. The selected option will be used by  the bot.

      ### Talk with me:
      To provide accurate advice, please provide the following details about the person involved in the criminal proceedings:

      1. Their **name**.
      2. The **proceeding language**.
      3. The **location** of the proceedings.
      4. Their **nationality**.
      5. Their **spoken language(s)**.
      6. Their **status** (e.g., suspect or accused).
      7. Whether they were **arrested/detained** by authorities.
      8. The **stage** of the proceedings (e.g., investigation, trial).
      9. Details of any **investigative events** (e.g., searches, interrogations).
      10. Any other **relevant information** about the case.

      Providing clear, complete information ensures tailored and effective legal guidance.
    """)

    if "chat_message" not in st.session_state:
      st.session_state.context = {
        "state" : "1",
        "person_id" : "",
        "directive_target" : "",
        "facts" : [],
        "rights" : {},
        "country_target" : "",
        "right_target" : "",
        "opt_target" : "",
        "target" : {},
        "arguments" : {},
        "pretty_arguments" : {},
        "suggestions" : set()
      }
      st.session_state.chat_message = []
      # st.session_state.memory = ConversationBufferWindowMemory(k=3, memory_key="my_chat", return_messages=True)
      st.session_state.memory = ConversationSummaryBufferMemory(llm=ChatGroq(
          groq_api_key='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',
          model_name="llama3-70b-8192",
          temperature=0.5
      ), max_token_limit=2000, memory_key="my_chat", return_messages=True)

    for message in st.session_state.chat_message:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    st.session_state.context["country_target"] = selected_law
    st.session_state.context["directive_target"] = selected_dir

    if user_question := st.chat_input("Describe your case:"):

        with st.chat_message("user"):
          st.markdown(user_question)

        st.session_state.chat_message.append({"role": "user", "content": user_question})

        select_state(st.session_state.chat_message, st.session_state.context)

        if st.session_state.context["state"] == "3":
          run_national_prolog(st.session_state.context)
          run_argumentation(st.session_state.context)
          suggest_facts(st.session_state.context)

        response = llm_response(user_question, st.session_state.context, st.session_state.memory)

        run_dir_prolog(response, st.session_state.context)

        with st.chat_message("ai"):
          st.markdown(response)

        st.session_state.chat_message.append({"role": "ai", "content": response})

if __name__ == "__main__":
    main()
