import json
import os
from datetime import datetime
import openai   # pip install openai

def quiz():
    data = []
    with open('game.txt', 'r', encoding='utf8') as file:
        for index, row in enumerate(file):
            if index == 0:
                continue
            text = row.strip('\"').split(sep='\",\"')
            question, right_answer = text[0], text[1]
            question_string = f'\nВопрос {index}.\n{question}\nВаш ответ?\n->'
            user_answer = input(question_string)
            data.append({'номер': index, 'вопрос': question, 'правильный ответ': right_answer,
                        'ответ студента': user_answer})
    return data

def save_result(name, ai_answers, student_answers):
    date = datetime.now().strftime("%d%m%Y")
    file = f'{name}-{date}.json'
    data = {"Студент": name, "Ответы студента": student_answers, "Ответы ИИ": ai_answers}
    with open(file, mode='w', encoding='utf-8') as file:
        json.dump(data, file)


def send_request_ai(answers):
    openai.api_key = os.getenv("OPENAI_KEY")
    response = openai.Completion.create(
    engine="gpt-4",
    prompt=f"""Проанализируй ответы студента: "{answers}",\nсравни с правильными ответами и выставь балл от 1 до 10
    в зависимости от правильности и полноты ответа, где 1 балл - ответ совершенно не правильный не полный,
    10 баллов - ответ правильный и полный. Ответ обоснуй. Формат ответа:
    Номер вопроса: (номер), Оценка: (балл). Комментарий: (обоснование)""",
    max_tokens=100,
    temperature=0.3
    )
    # return "10, Ofigenno!" # for tests
    return response.choices[0].text.strip()

def main():
    name = input("Викторина.\nВведите ваше имя: ")
    student_answers = quiz()
    ai_answers = send_request_ai(student_answers)
    save_result(name, ai_answers, student_answers)

if __name__ == "__main__":
    main()