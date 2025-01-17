import re
import os
import time
import json
from pathlib import Path
from groq import Groq

import input_facts

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

def extract_facts(user_text, directive, law, person_id=""):
  def _extract_code(completion):
    from mdextractor import extract_md_blocks
    blocks = extract_md_blocks(completion)
    return blocks[0] if blocks else ""

  res = prompt_model(f"""
    Assist the user in building a comprehensive case description by extracting relevant Prolog facts.
    There are certain facts which are essential and must always apply, unless explicitly stated otherwise:
    '''{input_facts.facts}'''.

    Consider also if any of the following conditions may be relevant:
    '''
    {input_facts.dir_facts[directive]}
    {input_facts.national_facts[directive][law]}
    '''

    Evaluate whether these facts can reasonably apply to the given scenario.

    Respect the following instructions:
    - DO NOT create new facts.
    - If the input is not relevant do not extract any fact

    Format of the output:
    - INCLUDE THE EXTRACTED PROLOG FACTS inside a single markdown block.
    - DO NOT create more than one block. Keep all facts in a single one.
    - DO NOT put comments inside the markdown block.
    - All variables must be lower letter for a fact to be valid.

    {"PersonId is " + person_id + "." if person_id else ""}

    Here is the user input:

    {user_text}
  """, temperature=0.01)

#   print(res)
#   print()

  return [x for x in [y.strip().split("%")[0] for y in _extract_code(res).replace(".", "").replace(" ", "").split("\n")] if x]

def parse_file(file_path, file_name):
  file_name_splits = file_name.replace(".txt", "").split("@")

  with open(os.path.join(file_path, file_name), "r") as f:
      text = f.read()

  facts_match = re.search(r"FACTS\n(.*?)\nFACTS_END", text, re.DOTALL)
  facts = [line.strip().replace(".", "").replace(" ", "") for line in facts_match.group(1).split("\n") if line.strip()] if facts_match else []

  test_match = re.search(r"TEST\n(.*?)\nTEST_END", text, re.DOTALL)
  tests = [re.sub(r"^\d+\.\s*", "", line.strip()) for line in test_match.group(1).split("\n") if line.strip()] if test_match else []

  return file_name_splits[0], file_name_splits[1], file_name_splits[2], facts, tests

def compute_raw_metrics(extracted, reference):
  extracted_set = set(extracted)
  reference_set = set(reference)

  true_positives = extracted_set.intersection(reference_set)
  false_positives = extracted_set.difference(reference_set)
  false_negatives = reference_set.difference(extracted_set)

  return len(true_positives), len(false_positives), len(false_negatives)

def compute_metrics(true_positives, false_positives, false_negatives):

  def _f_beta(beta, p, r):
    return (1 + beta**2) * (p * r) / ((beta**2 * p) + r) if p + r > 0 else 0

  precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
  recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
  res = {
    "true_positives" : true_positives,
    "false_positives" : false_positives,
    "false_negatives" : false_negatives,
    "precision" : precision,
    "recall": recall,
    "f1": _f_beta(1, precision, recall),
    "f2": _f_beta(2, precision, recall),
  }
  return res

def get_samples(tests, facts):
  n = 2 if len(facts) == 1 else 5
  return tests[:(n if len(tests) > n else len(tests))]

if __name__ == "__main__":
    path = os.path.join(Path(__file__).parent.absolute(), "..", "res", "extraction")
    files = [f for f in os.listdir(path)]

    true_positives = 0
    false_positives = 0
    false_negatives = 0

    res = {
      "partial" : {}
    }

    for file in files:
      directive, law, person_id, facts, tests = parse_file(path, file)

      t_r = {}
      temp_true_positives = 0
      temp_false_positives = 0
      temp_false_negatives = 0

      for i, test in enumerate(get_samples(tests, facts)):
        print(f"Computing scenario {i + 1} in {file}")
        extracted = extract_facts(test, directive, law, person_id)
        m = compute_raw_metrics(extracted, facts)
        temp_true_positives += m[0]
        temp_false_positives += m[1]
        temp_false_negatives += m[2]
        t_r[i] = {
          "input" : test,
          "extracted" : extracted
        }

      res["partial"][file] = {
        "facts" : facts,
        "metrics" : compute_metrics(temp_true_positives, temp_false_positives, temp_false_negatives),
        "test" : t_r
      }

      true_positives += temp_true_positives
      false_positives += temp_false_positives
      false_negatives += temp_false_negatives

    m = compute_metrics(true_positives, false_positives, false_negatives)
    print(f"Results: {m}")
    res["metrics"] = m
    with open(os.path.join(Path(__file__).parent.absolute(), "..", "res", f"results_{int(time.time())}.json"), "x") as f:
      json.dump(res, f, indent=4)
