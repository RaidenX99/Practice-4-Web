# -*- coding: utf-8 -*-
import streamlit as st
import json
import base64
import io
import re
import math
import random
from PIL import Image
from datetime import datetime
import plotly.graph_objects as go

from core import PracticeEngine

st.set_page_config(page_title="Практическая работа №4", layout="centered", page_icon="📉")

def parse_float(val_str):
    try:
        return float(val_str.strip().replace(',', '.'))
    except:
        return None

def draw_uniform_simulation(ans_str, text):
    val = parse_float(ans_str)
    
    match_a = re.search(r'a = (\d+)', text)
    match_b = re.search(r'b = (\d+)', text)
    match_t = re.search(r'X < (\d+)', text)
    
    a = int(match_a.group(1)) if match_a else 10
    b = int(match_b.group(1)) if match_b else 50
    t = int(match_t.group(1)) if match_t else 30
    
    height = 1 / (b - a)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[a, b, b, a, a], y=[0, 0, height, height, 0], fill='toself', mode='lines', line_color='rgba(150,150,150,0.5)', name='Плотность f(x)'))
    
    if val is not None and 0 <= val <= 1:
        x_calc = a + val * (b - a)
        fig.add_trace(go.Scatter(x=[a, x_calc, x_calc, a, a], y=[0, 0, height, height, 0], fill='toself', mode='lines', fillcolor='rgba(0, 200, 100, 0.6)', line_color='green', name='Ваша вероятность'))
    elif val is not None:
        fig.add_trace(go.Scatter(x=[a, b, b, a, a], y=[0, 0, height, height, 0], fill='toself', mode='lines', fillcolor='rgba(255, 0, 0, 0.6)', line_color='red', name='Ошибка'))

    fig.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10), title="Равномерное распределение")
    st.plotly_chart(fig, use_container_width=True)

def draw_exponential_simulation(ans_str, text):
    val = parse_float(ans_str)
    
    match_lam = re.search(r'λ = (0\.\d+)', text)
    match_t = re.search(r't = (\d+)', text)
    
    lam = float(match_lam.group(1)) if match_lam else 0.02
    t_target = int(match_t.group(1)) if match_t else 50
    
    t_vals = list(range(0, t_target * 3))
    r_vals = [math.exp(-lam * t) for t in t_vals]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_vals, y=r_vals, mode='lines', line=dict(color='blue', width=3), name='R(t)'))
    
    if val is not None and 0 <= val <= 1:
        color = 'green'
        fig.add_trace(go.Scatter(x=[t_target], y=[val], mode='markers', marker=dict(color=color, size=14, line=dict(width=2, color='white')), name='Ваш расчет'))

    fig.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10), title="Функция надежности (Экспонента)")
    st.plotly_chart(fig, use_container_width=True)

def draw_normal_simulation(ans_str):
    val = parse_float(ans_str)
    
    x = [i/10.0 for i in range(-40, 41)]
    y = [math.exp(-0.5 * ((v/10)**2)) for v in x]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='rgba(100,150,250,0.8)', width=3), name='f(x)'))
    
    if val is not None:
        if val < 0 or val > 1:
            fig.add_trace(go.Scatter(x=x, y=y, fill='tozeroy', mode='none', fillcolor='rgba(255, 0, 0, 0.4)', name='Ошибка'))
        else:
            center = len(x) // 2
            limit = int((len(x) / 2) * val)
            fill_x = x[center-limit:center+limit+1]
            fill_y = y[center-limit:center+limit+1]
            if fill_x:
                fig.add_trace(go.Scatter(x=fill_x, y=fill_y, fill='tozeroy', mode='none', fillcolor='rgba(0, 200, 100, 0.5)', name='Ваша площадь'))

    fig.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10), title="Нормальное распределение (Ping)", xaxis=dict(showgrid=False, zeroline=False, showticklabels=False), yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
    st.plotly_chart(fig, use_container_width=True)

def draw_threesigma_simulation(ans_str, text):
    parts = str(ans_str).split()
    
    match_a = re.search(r'a = (\d+)', text)
    match_sig = re.search(r'σ = (\d+)', text)
    a = int(match_a.group(1)) if match_a else 500
    sig = int(match_sig.group(1)) if match_sig else 20
    
    x = list(range(a - 4*sig, a + 4*sig))
    y = [math.exp(-0.5 * (((v - a)/sig)**2)) for v in x]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='gray', width=2), name='Трафик'))
    
    if len(parts) == 2:
        try:
            s_min, s_max = float(parts[0]), float(parts[1])
            fill_x = [v for v in x if s_min <= v <= s_max]
            fill_y = [math.exp(-0.5 * (((v - a)/sig)**2)) for v in fill_x]
            if fill_x:
                fig.add_trace(go.Scatter(x=fill_x, y=fill_y, fill='tozeroy', mode='none', fillcolor='rgba(0, 200, 100, 0.4)', name='Ваш интервал'))
            
            anom_x1 = [v for v in x if v < s_min]
            anom_y1 = [math.exp(-0.5 * (((v - a)/sig)**2)) for v in anom_x1]
            if anom_x1:
                fig.add_trace(go.Scatter(x=anom_x1, y=anom_y1, fill='tozeroy', mode='none', fillcolor='rgba(255, 0, 0, 0.5)', showlegend=False))
                
            anom_x2 = [v for v in x if v > s_max]
            anom_y2 = [math.exp(-0.5 * (((v - a)/sig)**2)) for v in anom_x2]
            if anom_x2:
                fig.add_trace(go.Scatter(x=anom_x2, y=anom_y2, fill='tozeroy', mode='none', fillcolor='rgba(255, 0, 0, 0.5)', showlegend=False))
        except:
            pass

    fig.update_layout(height=250, margin=dict(l=10, r=10, t=30, b=10), title="Детектор аномалий (3 Сигмы)")
    st.plotly_chart(fig, use_container_width=True)

if 'started' not in st.session_state:
    st.session_state.started = False
    st.session_state.student_id = ""
    st.session_state.start_time = None
    st.session_state.report_json = None
    st.session_state.filename = ""

if not st.session_state.started:
    st.title("📉 Практическая работа №4 - ТВиМС")
    st.write("Непрерывные случайные величины (НСВ) и законы их распределения")
    
    with st.container():
        st.info("Введите номер вашей зачетной книжки. От этого номера зависит ваш уникальный вариант.")
        student_id_input = st.text_input("Номер зачетной книжки:", placeholder="Например: 220156")
        
        if st.button("🚀 Начать практику", use_container_width=True):
            if student_id_input.strip():
                st.session_state.student_id = student_id_input.strip()
                st.session_state.started = True
                st.session_state.start_time = datetime.now()
                st.rerun()
            else:
                st.error("Поле не может быть пустым!")

elif st.session_state.started and st.session_state.report_json is None:
    st.title(f"🎓 Практика №4 | Зачетка: {st.session_state.student_id}")
    
    engine = PracticeEngine(st.session_state.student_id)
    variant = engine.generate_variant()
    
    st.warning("⚠️ Для зачета каждой задачи ОБЯЗАТЕЛЬНО необходимо прикрепить фотографию рукописного решения! Можно прикреплять несколько фото.")
    
    if 'student_answers' not in st.session_state:
        st.session_state.student_answers = {}
    if 'student_photos' not in st.session_state:
        st.session_state.student_photos = {}

    for task_key, task_data in variant.items():
        st.divider()
        if task_key == 'task_99':
            st.markdown(f"### 📝 {task_data['title']}")
            st.write(task_data['text'])
            ans = st.text_input("Краткий комментарий (необязательно):", key=f"ans_{task_key}")
            st.session_state.student_answers[task_key] = ans
            photos = st.file_uploader("📸 Прикрепить фото с ответами (можно несколько)", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key=f"photo_{task_key}")
            st.session_state.student_photos[task_key] = photos
        else:
            task_num = task_key.split('_')[1]
            st.markdown(f"### 🔹 Задача {task_num}")
            st.write(task_data['text'])
            
            ans = st.text_input("Ваш ответ:", key=f"ans_{task_key}")
            st.session_state.student_answers[task_key] = ans
            
            if task_key == 'task_1':
                draw_uniform_simulation(ans, task_data['text'])
            elif task_key == 'task_2':
                draw_exponential_simulation(ans, task_data['text'])
            elif task_key == 'task_3':
                draw_normal_simulation(ans)
            elif task_key == 'task_4':
                draw_threesigma_simulation(ans, task_data['text'])
                
            photos = st.file_uploader("📸 Прикрепить решение (можно несколько фото)", type=["jpg", "jpeg", "png"], accept_multiple_files=True, key=f"photo_{task_key}")
            st.session_state.student_photos[task_key] = photos
        
    st.divider()
    if st.button("✅ Завершить и сформировать отчет", use_container_width=True, type="primary"):
        delta = datetime.now() - st.session_state.start_time
        mins = int(delta.total_seconds() // 60)
        secs = int(delta.total_seconds() % 60)
        time_spent_str = f"{mins} мин. {secs} сек."
        
        student_answers_raw = {}
        encrypted_answers = {}
        
        for k, text_val in st.session_state.student_answers.items():
            raw_val = text_val.strip().replace(',', '.')
            student_answers_raw[k] = raw_val
            encrypted_answers[k] = base64.b64encode(raw_val[::-1].encode('utf-8')).decode('utf-8')
            
        for k, file_list in st.session_state.student_photos.items():
            if file_list: 
                compressed_photos = []
                encrypted_photos = []
                for file in file_list:
                    img = Image.open(file).convert("RGB")
                    img.thumbnail((1200, 1200))
                    buffered = io.BytesIO()
                    img.save(buffered, format="JPEG", quality=75)
                    b64_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
                    compressed_photos.append(b64_str)
                    encrypted_photos.append(base64.b64encode(b64_str[::-1].encode('utf-8')).decode('utf-8'))
                
                student_answers_raw[f"{k}_photo"] = compressed_photos
                encrypted_answers[f"{k}_photo"] = encrypted_photos
                
        security_hash = engine.generate_security_hash(engine.student_id, student_answers_raw)
        
        report_data = {
            "student_id": engine.student_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "time_spent": time_spent_str,
            "answers": encrypted_answers,
            "verification_key": security_hash
        }
        
        st.session_state.report_json = json.dumps(report_data, ensure_ascii=False, indent=4)
        st.session_state.filename = f"Отчет_Практика4_{engine.student_id}.json"
        st.rerun()

if st.session_state.get('report_json') is not None:
    st.title("🎉 Работа успешно завершена!")
    st.success("Отчет зашифрован и сформирован. Скачайте файл и отправьте его преподавателю.")
    st.download_button(
        label="📥 СКАЧАТЬ ФАЙЛ ОТЧЕТА (.json)",
        data=st.session_state.report_json,
        file_name=st.session_state.filename,
        mime="application/json",
        use_container_width=True
    )
    if st.button("Выйти на главную"):
        st.session_state.started = False
        st.session_state.report_json = None
        st.rerun()