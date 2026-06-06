# AI Agent Definitions and LLM Interactions
from openai import OpenAI
from config import API_KEY, BASE_URL, MODEL

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)

def ask_ai(prompt):
    """Base function to call the LLM and return text."""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

def validate_case(crime_description):
    """Checks if the input is a valid case or just nonsense/small talk."""
    prompt = f"Analyze if the following input describes a plausible scenario, crime, or violation that could be argued in court. If it's a simple greeting (like 'how are you'), a math fact ('2+2=4'), or completely unrelated to a legal or rule-breaking context, you must reject it.\n\nInput: '{crime_description}'\n\nRespond EXACTLY with 'VALID' if it can be debated, or 'INVALID: <brief reason>' if it cannot."
    response = ask_ai(prompt)
    if response.strip().upper().startswith("VALID"):
        return True, ""
    else:
        reason = response.replace("INVALID:", "").replace("INVALID", "").strip()
        return False, reason

def generate_prosecutor_statement(crime_description, previous_argument=None):
    """Generates an argument for the Cyber-Prosecutor."""
    if not previous_argument:
        prompt = f"You are a Cyber-Prosecutor in a courtroom. The crime is: {crime_description}. Write a clear and strong 1-paragraph opening statement explaining why the defendant is guilty. Use simple, easy-to-understand English. Keep it short and to the point."
    else:
        prompt = f"You are a Cyber-Prosecutor in a courtroom. The crime is: {crime_description}. The Defense just argued: '{previous_argument}'. Write a clear 1-paragraph counter-argument in simple English. Point out the weaknesses in their defense."
    return ask_ai(prompt)

def generate_defense_statement(crime_description, previous_argument):
    """Generates an argument for the Defense Attorney."""
    prompt = f"You are a Defense Lawyer in a courtroom. The crime is: {crime_description}. The Prosecutor just argued: '{previous_argument}'. Write a clear 1-paragraph rebuttal in simple, easy-to-understand English. Find logical flaws or missing evidence in their argument."
    return ask_ai(prompt)

def generate_judge_verdict(crime_description, debate_history, jury_vote):
    """Generates the final verdict from the Judge, evaluating if the jury was correct."""
    history_text = "\n".join([f"{m['role']}: {m['text']}" for m in debate_history])
    prompt = f"""You are the Supreme Cyber-Court Judge. 
The crime is: {crime_description}.
Here is the transcript of the debate:
{history_text}

The human jury has voted: {jury_vote}.

Your task is to:
1. Objectively evaluate the arguments presented by the Prosecution and Defense. Decide which side made a stronger, more logical case based ONLY on the debate transcript.
2. Compare your conclusion to the jury's vote. 
3. If the jury's vote is justified by the debate, agree with them and deliver the verdict. 
4. If the jury's vote is completely wrong or ignores the stronger arguments, you MUST OVERRULE the jury. Explain why their decision was flawed, and deliver the correct verdict instead.

Write your final ruling in 2-3 short paragraphs using simple, clear, and dramatic language. 
Start with 'THIS COURT FINDS THE DEFENDANT [GUILTY / NOT GUILTY]...'"""
    return ask_ai(prompt)
