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
        rng = random.Random(self.seed)
        pool = []

        # 1. Наивероятнейшее число попаданий (схема Бернулли)
        n1 = 10
        p1 = 0.2
        k0 = int((n1 + 1) * p1)
        pool.append({
            'text': f"Производится $n = {n1}$ независимых проверок сетевого узла, вероятность успешного отклика в каждом равна $p = {p1}$. Найти наивероятнейшее число успешных откликов $k_0$. (Введите целое число).",
            'answer': str(k0)
        })

        # 2. Вероятность попадания в интервал (не менее k)
        p2 = 0.25
        n2 = 8
        ans2 = sum(math.comb(n2, k) * (p2**k) * ((1-p2)**(n2-k)) for k in range(6, n2+1))
        pool.append({
            'text': f"Вероятность случайного попадания запроса в защитный фильтр равна $p = {p2}$. Сбрасывается 8 независимых запросов. Найти вероятность того, что будет не менее 6 успешных блокировок. (Округление до 4 знаков).",
            'answer': str(round(ans2, 4))
        })

        # 3. Пуассоновский поток: ноль сбоев за двое суток
        lam3 = 1.5
        ans3 = math.exp(-2 * lam3)
        pool.append({
            'text': f"Среднее число сбоев маршрутизатора за сутки равно $\\lambda = {lam3}$. Найти вероятность того, что за двое суток не будет ни одного сбоя ($k = 0$). (Округление до 4 знаков).",
            'answer': str(round(ans3, 4))
        })

        # 4. Пуассоновский поток: хотя бы один сбой за сутки
        ans4 = 1 - math.exp(-lam3)
        pool.append({
            'text': f"Среднее число сбоев маршрутизатора за сутки равно $\\lambda = {lam3}$. Найти вероятность того, что в течение суток произойдет хотя бы один сбой ($k \ge 1$). (Округление до 4 знаков).",
            'answer': str(round(ans4, 4))
        })

        # 5. Пуассоновский поток за неделю (не менее трех сбоев)
        lam_week = lam3 * 7
        ans5 = 1 - (math.exp(-lam_week) + lam_week * math.exp(-lam_week) + (lam_week**2 / 2) * math.exp(-lam_week))
        pool.append({
            'text': f"Среднее число сбоев за сутки равно $\\lambda = {lam3}$. Найти вероятность того, что за неделю (7 дней) работы оборудования произойдет не менее трех сбоев ($k \ge 3$). (Округление до 4 знаков).",
            'answer': str(round(ans5, 4))
        })

        # 6. Математическое ожидание дискретной случайной величины
        x_vals = [-2, -1, 0, 1, 2]
        p_vals = [0.1, 0.2, 0.2, 0.4, 0.1]
        mx = sum(x*p for x, p in zip(x_vals, p_vals))
        pool.append({
            'text': f"Случайная величина $X$ задана законом распределения:\n$X$: {-2}, {-1}, {0}, {1}, {2}\n$P$: {0.1}, {0.2}, {0.2}, {0.4}, {0.1}\nНайти математическое ожидание $M(X)$. (Округление до 2 знаков).",
            'answer': str(round(mx, 2))
        })

        # 7. Дисперсия дискретной случайной величины
        dx = sum((x**2)*p for x, p in zip(x_vals, p_vals)) - mx**2
        pool.append({
            'text': f"Для той же случайной величины $X$ (с тем же законом распределения) найти дисперсию $D(X)$. (Округление до 2 знаков).",
            'answer': str(round(dx, 2))
        })

        # 8. Вероятность абсолютного значения P(|X| <= 1)
        p_abs = sum(p for x, p in zip(x_vals, p_vals) if abs(x) <= 1)
        pool.append({
            'text': f"Для той же случайной величины $X$ найти вероятность $P(|X| \\le 1)$. (Округление до 2 знаков).",
            'answer': str(round(p_abs, 2))
        })

        # 9. Геометрическое распределение (попытки до первого успеха)
        p_geom = 0.2
        ans9 = (1 - p_geom)**2 * p_geom
        pool.append({
            'text': f"Передача пакетов по каналу связи повторяется до первого успешного подтверждения (ACK). Вероятность сбоя в отдельной попытке равна $q = {1 - p_geom}$, а успех $p = {p_geom}$. Найти вероятность того, что первый успех наступит ровно на 3-й попытке ($k = 3$). (Округление до 4 знаков).",
            'answer': str(round(ans9, 4))
        })

        # 10. Биномиальное распределение (точно k успехов)
        n10 = 10
        p10 = 0.2
        k10 = 3
        ans10 = math.comb(n10, k10) * (p10**k10) * ((1-p10)**(n10-k10))
        pool.append({
            'text': f"В серии из $n = {n10}$ независимых испытаний вероятность успеха в каждом равна $p = {p10}$. Найти вероятность того, что будет ровно $k = {k10}$ успехов. (Округление до 4 знаков).",
            'answer': str(round(ans10, 4))
        })

        # 11-20. Дополнительные расчетные задачи
        for i in range(11, 21):
            n_v = 10
            p_v = round(rng.uniform(0.1, 0.4), 2)
            k_v = rng.randint(1, 4)
            ans_v = math.comb(n_v, k_v) * (p_v**k_v) * ((1-p_v)**(n_v-k_v))
            pool.append({
                'text': f"Тестовый узел выполняет $n = {n_v}$ операций, вероятность ошибки в каждой равна $p = {p_v}$. Найти вероятность ровно $k = {k_v}$ ошибок. (Округление до 4 знаков).",
                'answer': str(round(ans_v, 4))
            })

        rng.shuffle(pool)
        variant = {}
        for idx, task_item in enumerate(pool):
            variant[f"task_{idx+1}"] = task_item

        cq_pool = [
            "Что такое дискретная случайная величина и как задается ее закон распределения?",
            "Дайте определение функции распределения $F(x)$ дискретной случайной величины и перечислите ее свойства.",
            "В чем заключается физический смысл и формула биномиального распределения?",
            "Как определяются математическое ожидание и дисперсия для биномиального закона?",
            "При каких условиях применяется закон Пуассона и каково его математическое ожидание?",
            "Опишите геометрическое распределение дискретной случайной величины."
        ]
        variant['task_99'] = {
            'title': 'Контрольный теоретический вопрос',
            'text': f"ОБЯЗАТЕЛЬНО прикрепите фото с развернутым рукописным ответом на вопрос:\n\n{rng.choice(cq_pool)}",
            'answer': 'Ручная проверка (Требуется фото)'
        }
        return variant

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

        def is_close(val1, val2, tol=0.01):
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
                    details[task_key] = {'is_correct': True, 'correct_answer': "Фото прикреплено", 'student_answer': f"Фото ({len(photo_list)} шт.)"}
                else:
                    details[task_key] = {'is_correct': False, 'correct_answer': "Требуется фото", 'student_answer': "Нет фото!"}
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
