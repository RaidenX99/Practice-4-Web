# -*- coding: utf-8 -*-
import random
import math
import hashlib
import json

SECRET_SALT = "Ural_Telecom_2026_Secret"

class PracticeEngine:
    def __init__(self, student_id: str):
        self.student_id = student_id.strip().upper()
        self.seed = self._generate_seed()
        random.seed(self.seed)

    def _generate_seed(self):
        hash_obj = hashlib.md5(self.student_id.encode())
        return int(hash_obj.hexdigest(), 16)

    def generate_variant(self) -> dict:
        variant = {}
        
        variant['task_1'] = self._task_1_uniform()
        variant['task_2'] = self._task_2_exponential()
        variant['task_3'] = self._task_3_normal()
        variant['task_4'] = self._task_4_three_sigma()
        
        cq_pool = [
            "Дайте определение непрерывной случайной величины (НСВ). Чем она отличается от дискретной?",
            "Что такое плотность распределения вероятностей f(x) и какими свойствами она обладает?",
            "Как связаны функция распределения F(x) и плотность распределения f(x) для НСВ?",
            "Запишите плотность равномерного распределения. Чему равны его математическое ожидание и дисперсия?",
            "Запишите функцию надежности R(t) для показательного распределения и объясните смысл параметра λ.",
            "Как выглядит график плотности нормального распределения (кривая Гаусса) и как на него влияют параметры a и σ?",
            "Сформулируйте правило «трех сигм» для нормального распределения. Каков его практический смысл?"
        ]
        
        selected_questions = random.sample(cq_pool, 3)
        questions_text = "\n".join([f"{i+1}. {q}" for i, q in enumerate(selected_questions)])
        
        variant['task_99'] = {
            'title': 'Контрольные теоретические вопросы (НСВ)',
            'text': f"ОБЯЗАТЕЛЬНО прикрепите фото с развернутым рукописным ответом на следующие вопросы:\n\n{questions_text}",
            'answer': 'Ручная проверка (Требуется фото)'
        }
        
        return variant

    def _task_1_uniform(self):
        a = random.randint(10, 20)
        b = random.randint(50, 80)
        t = random.randint(a + 10, b - 10)
        
        text = f"Время плановой перезагрузки маршрутизатора Cisco (в секундах) есть непрерывная случайная величина X, распределенная РАВНОМЕРНО в интервале от a = {a} до b = {b}. Найти вероятность того, что маршрутизатор перезагрузится быстрее, чем за {t} секунд (т.е. X < {t}). (Ответ округлите до 4 знаков)."
        
        ans = (t - a) / (b - a)
        return {'text': text, 'answer': str(round(ans, 4))}

    def _task_2_exponential(self):
        lam = round(random.uniform(0.01, 0.05), 3)
        t = random.choice([24, 48, 72, 100])
        
        text = f"Время безотказной работы коммутатора в лаборатории связи подчиняется ПОКАЗАТЕЛЬНОМУ закону распределения с интенсивностью отказов λ = {lam} (1/час). Вычислить функцию надежности R(t) — вероятность того, что коммутатор проработает без сбоев t = {t} часов. (Ответ округлите до 4 знаков)."
        
        ans = math.exp(-lam * t)
        return {'text': text, 'answer': str(round(ans, 4))}

    def _task_3_normal(self):
        a = random.randint(40, 60)
        sigma = random.randint(4, 8)
        
        x1 = a - sigma * random.choice([1, 2])
        x2 = a + sigma * random.choice([1, 1.5, 2])
        
        text = f"Задержка сигнала (Ping) до удаленного сервера распределена НОРМАЛЬНО. Математическое ожидание a = {a} мс, среднее квадратическое отклонение σ = {sigma} мс. Используя таблицы функции Лапласа Ф(x), вычислить вероятность того, что задержка очередного пакета окажется в коридоре от {x1} до {x2} мс. (Ответ округлите до 4 знаков)."
        
        t1 = (x1 - a) / sigma
        t2 = (x2 - a) / sigma
        
        phi_t1 = math.erf(t1 / math.sqrt(2)) / 2
        phi_t2 = math.erf(t2 / math.sqrt(2)) / 2
        ans = phi_t2 - phi_t1
        
        return {'text': text, 'answer': str(round(ans, 4))}

    def _task_4_three_sigma(self):
        a = random.randint(400, 800)
        sigma = random.randint(15, 35)
        
        text = f"Настраиваются триггеры безопасности Zabbix. Входящий трафик распределен нормально со средним значением a = {a} Мбит/с и отклонением σ = {sigma} Мбит/с. Используя «Правило трех сигм», рассчитайте доверительный интервал штатной работы сети [X_min; X_max], выход за который с вероятностью 0.9973 будет признан аномалией (DDoS-атакой). \nВ ответе запишите через пробел нижнюю и верхнюю границы. (Пример: 350 550)."
        
        ans_min = a - 3 * sigma
        ans_max = a + 3 * sigma
        
        return {'text': text, 'answer': f"{ans_min} {ans_max}"}

    @staticmethod
    def generate_security_hash(student_id: str, student_answers: dict) -> str:
        answers_str = json.dumps(student_answers, sort_keys=True)
        raw_data = f"{student_id}_{answers_str}_{SECRET_SALT}"
        return hashlib.sha256(raw_data.encode('utf-8')).hexdigest()

    def check_answers(self, student_answers: dict) -> dict:
        variant = self.generate_variant()
        correct_count = 0
        total_count = len(variant)
        details = {}

        def is_close(val1, val2, tol=0.005):
            if ' ' in str(val1) and ' ' in str(val2):
                parts1 = str(val1).split()
                parts2 = str(val2).split()
                if len(parts1) == len(parts2):
                    return all(abs(float(p1) - float(p2)) <= tol for p1, p2 in zip(parts1, parts2))
                return False
            try:
                return abs(float(val1) - float(val2)) <= tol
            except ValueError:
                return str(val1).strip().lower() == str(val2).strip().lower()

        for task_key, task_data in variant.items():
            photo_list = student_answers.get(f"{task_key}_photo", [])
            has_photo = bool(photo_list)
            
            student_ans_str = student_answers.get(task_key, "").strip().replace(',', '.')
            correct_ans_str = str(task_data.get('answer', ''))
            
            if task_key == 'task_99':
                if has_photo:
                    is_correct = True
                    correct_count += 1
                    details[task_key] = {
                        'is_correct': True, 'correct_answer': "Фото прикреплено",
                        'student_answer': f"Фото ({len(photo_list)} шт.)"
                    }
                else:
                    details[task_key] = {
                        'is_correct': False, 'correct_answer': "Требуется фото",
                        'student_answer': "Нет фото!"
                    }
                continue

            is_correct = is_close(student_ans_str, correct_ans_str)

            if not has_photo:
                is_correct = False
                student_ans_str = f"{student_ans_str} (Нет фото!)" if student_ans_str else "Нет ответа (Нет фото!)"

            if is_correct: correct_count += 1
            details[task_key] = {'is_correct': is_correct, 'correct_answer': correct_ans_str, 'student_answer': student_ans_str}

        score_percent = (correct_count / total_count) * 100
        if score_percent >= 85: mark = 5
        elif score_percent >= 70: mark = 4
        elif score_percent >= 50: mark = 3
        else: mark = 2

        photos_dict = {k: student_answers.get(f"{k}_photo") for k in variant.keys() if student_answers.get(f"{k}_photo")}

        return {
            'correct_count': correct_count,
            'total_count': total_count,
            'percent': round(score_percent, 1),
            'mark': mark,
            'details': details,
            'photos': photos_dict
        }