import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    matches = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

botname = "Hammam"

def handle_user_input(user_input: str, knowledge_base: dict) -> str:
    best_match = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])
    if best_match:
        answer = get_answer_for_question(best_match, knowledge_base)
        return answer if answer else "Sorry, I don't know the answer to that question."
    else:
        return "I don't know the answer. Can you teach me?"

def add_new_answer(user_input: str, new_answer: str, knowledge_base: dict):
    knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
    save_knowledge_base("knowledge_base.json", knowledge_base)
    return "Thank you, I have learned a new response."

def chat_bot(user_input: str) -> str:
    knowledge_base = load_knowledge_base('knowledge_base.json')
    response = handle_user_input(user_input, knowledge_base)
    return response