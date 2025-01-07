import re
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


def arg_hash(context):
    hash(f"{context["target"]} - {context["national_target"]} - {context["facts"]}")


def select_prompt(context):

    return f"""
      Follow all instructions of Phase 1, before Phase 2.

      Phase 1: Interacting with the user.
      Assist the user in building a comprehensive case description by extracting relevant Prolog facts, while conversing with the user.
      There are certain facts which are essential and must always apply, unless explicitly stated otherwise: '''{input_facts.facts}'''.

      There are other conditions which you shall evaluate whether these facts can reasonably apply to the given scenario,
      considering any relevant conditions and context :'''{input_facts.facts_dir_2013_48}'''.

      Use the fact to verify if it is possible it may apply to the given scenario.
      You can assume that some facts are present if similar or connected facts apply.
      Avoid asking yes or no questions.

      Respect the following instructions:
      - DO NOT create new facts.
      - DO NOT tell the user what rights may apply.
      - DO NOT ask similar questions more than once.

      Format of the output:
      - Include the list of Prolog facts extracted inside a single markdown block.
      - DO NOT create more than one block. Keep all facts in a single one.
      - DO NOT put comments inside the markdown block.
      - All variables must be lower letter for a fact to be valid.

      After some questions ask the users if she wants to know what rights she has.

    """ + (f"""
      Phase 2: Presenting the rights computed by the symbolic engine.
           Present the user the following lists of rights separately.

      - Rights granted at the EUROPEAN level: {[k for k, _ in context["rightsD"].items()]}

      - Rights recognised at NATIONAL level: {[k for k, _ in context["rightsN"].items()]}

      Ask if the user wants to know more details any of these rights.

    """ if context["state"] == "2" else "") + (f"""

      Phase 3: Explaining the Rights

      These are the details on {context["target"]}:

      {context["rights"][context["target"]]}

      The right has a label, a corresponding article, and an option (specific application).
      One right can have multiple options. Show all the options.

      For each right, follow these instructions:
      - Explain what each right refers to.
      - Tell the user the article and source of origin.
      - Give a summary of the relevant facts which grant the specific right.

      Ask if the user wants to know about the conformity evaluation with the European country about any right.

      Respect the following instructions:
      - DO NOT create new rights.
      - DO NOT provide legal advice.

    """ if context["target"] else "") + (f"""

      Arguments on conformity with national implementations [{context["national_target"]}]:

      {context["arguments"][arg_hash(context)]}

      Questions on conformity can only be answered based on these arguments. Do not add anything.

      There are three levels of conformity:
      - Full Conformity ((conformity(COUNTRY, ART)): All rights and conditions are identical between EU and national implementation.
      - No Conformity ('-'(conformity(COUNTRY, ART)): No rights are granted under the national implementation.
      - Partial Conformity (partial_conformity(COUNTRY, ART)): Rights are granted, but under different conditions than the european source.

      These are some specific and additional facts required by the national implementation: {context["suggestions"]}

    """ if context["target"] and context["national_target"] else "")


def select_state(input, context):
    res = prompt_model(f"""
        According to the following input, what does the user want to do?

        1. Input new facts into the system;
        2. Know which rights are deducible from her scenario;
        3. Know about one of this specific rights: {[k for k, _ in context["rights"].items()]}

        Reply "1" if 1, "2" if 2, and "3 - right from the list" if 3.
        Do not include anything else in your output.

        {input}
    """)

    context["target"] = [x.strip() for x in res.split("-")][1] if "3" in res else context["target"]
    context["state"] = "1" if "1" in res else "2" if "2" in res else "3"


def run_argumentation(context):
    if context["target"] and context["national_target"] and arg_hash(context) not in context["arguments"]:
      theory = get_full_theory("\n".join([x["arg_rule"] for _, v in context["rights"][context["target"]].items() for x in v]), [context["national_target"]])
      context["arguments"][arg_hash(context)] = run_reasoner(theory)
      print(context["arguments"][arg_hash(context)])


def parse_output(user_text):

  def _extract_code(completion):
    from mdextractor import extract_md_blocks
    blocks = extract_md_blocks(completion)
    return blocks[0] if blocks else ""

  return [x for x in _extract_code(user_text).replace(".", "").split("\n") if x]


def run_prolog(output, context):
  try:
    user_facts = parse_output(output)
    if user_facts:
      context["person_id"] = re.search(r"person_status\((.+),", "\n".join(user_facts)).group(1).strip()
      facts, prolog_responseD = generate_response(context["person_id"], user_facts, ["dir"])
      xt["person_id"], user_facts, [facts, prolog_responseN = generate_response(contecontext["national_target"]] if context["national_target"] else [])
      prettyD = prettify_response(prolog_responseD, facts)
      prettyN = prettify_response(prolog_responseN, facts)
      context["rightsD"] = prettyD
      context["rightsN"] = prettyN
      context["facts"] = user_facts
      context["rights"] = {**prettyD, **prettyN}
      print(context["person_id"])
      print(context["facts"])
      print("Directive:\n")
      print(context["rightsD"])
      print("National:\n")
      print(context["rightsN"])
  except Exception as e:
    print(e)


def suggest_facts(context):
  if not context["national_target"] or not context["target"] or not context["person_id"]:
     return
  try:
      facts, prolog_response = generate_response(context["person_id"], context["facts"], [context["national_target"]], right=context["target"], abduce=True)
      pretty = prettify_response(prolog_response, facts)
      abduced = set([y for _, v in pretty[context["target"]].items() for x in v for y in x["abduced"]])
      context["suggestions"] = abduced
      print("Abduction result:")
      print(abduced)
  except Exception as e:
    print(e)


def llm_response(input_text, context, memory):
  return LLMChain(
      llm=ChatGroq(
          groq_api_key='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',
          model_name="llama3-70b-8192"
      ),
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

    st.title("Chat with CrossJustice!")

    if "chat_message" not in st.session_state:
      st.session_state.context = {
        "facts" : [],
        "rights" : {},
        "rightsD" : {},
        "rightsN" : {},
        "target" : "",
        "arguments" : {},
        "person_id" : "",
        "national_target" : "nl",
        "state" : "1",
        "suggestions" : set()
      }
      st.session_state.chat_message = []
      st.session_state.memory = ConversationBufferWindowMemory(k=3, memory_key="my_chat", return_messages=True)

    for message in st.session_state.chat_message:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_question := st.chat_input("Describe your case:"):

        with st.chat_message("user"):
          st.markdown(user_question)

        st.session_state.chat_message.append({"role": "user", "content": user_question})

        select_state(user_question, st.session_state.context)
        print(st.session_state.context["state"])

        run_argumentation(st.session_state.context)
        suggest_facts(st.session_state.context)

        # if st.session_state.context["state"] == "1":
        #   st.session_state.context["rights"] = {}
        #   st.session_state.context["target"] = ""

        response = llm_response(user_question, st.session_state.context, st.session_state.memory)

        run_prolog(response, st.session_state.context)

        with st.chat_message("ai"):
          st.markdown(response)

        st.session_state.chat_message.append({"role": "ai", "content": response})

if __name__ == "__main__":
    main()
