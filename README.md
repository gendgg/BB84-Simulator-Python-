=== RUS ===

## 🔐 Квантовый криптографический симулятор BB84

Интерактивный образовательный симулятор протокола квантового распределения ключей BB84 с графическим интерфейсом. Проект предназначен для изучения основ квантовой криптографии, влияния шума канала (декогеренции) и атак перехвата (Eve's attack) на безопасность связи.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Qiskit](https://img.shields.io/badge/Qiskit-Optional-purple.svg)

## 📸 Скриншоты / Screenshots
 1. Вкладка BB84 /  BB84 Tab::
   <img width="1823" height="1080" alt="image" src="https://github.com/user-attachments/assets/64d5f03e-aad6-4a67-8212-e9000b286afc" />

 2. Атака Евы / Eve's Attack::
   <img width="1825" height="1080" alt="image" src="https://github.com/user-attachments/assets/8476106f-6477-4a64-9d62-ed5f979f6adc" />

 3. Генерация и сравнение ключей / Key Generation and Comparison::
   <img width="1824" height="1080" alt="image" src="https://github.com/user-attachments/assets/061a2af5-9c33-4ecd-b29b-05d416a82b46" />

 4. Графики / Graphs::
   <img width="1823" height="1080" alt="image" src="https://github.com/user-attachments/assets/101a3c8b-bee6-48b3-9dca-735f68036c32" />

 5. Результаты измерений и соответствующие им выводы /  Measurement Results and Conclusions::
    <img width="1822" height="1080" alt="image" src="https://github.com/user-attachments/assets/915ef163-2937-434e-973b-9f13f5afb05d" />


## ✨ Возможности
- **Симуляция протокола BB84:** Генерация квантового ключа с учетом выбора базисов Алисой и Бобом.
- **Моделирование шума канала:** Настройка уровня естественного шума (декогеренции) и наблюдение за его влиянием на QBER (Quantum Bit Error Rate).
- **Атака Евы:** Визуализация перехвата фотонов и демонстрация того, почему подслушивание в квантовой криптографии всегда оставляет следы (порог обнаружения ~11%).
- **Генерация энтропии:** Сравнение простого генератора случайных чисел с гибридным методом (время, хаотические системы, системные параметры).
- **Визуализация:** Построение графиков зависимости QBER от силы атаки с использованием `matplotlib`.
- **Поддержка Qiskit:** Если установлена библиотека Qiskit, симуляция использует реальные квантовые схемы (волновые векторы), иначе работает в упрощенном вероятностном режиме.

## 🚀 Установка и запуск

# 1. Клонируем репозиторий и переходим в его папку (замените URL на ссылку вашего репозитория)
git clone https://github.com/gendgg/project.git
cd project

# 2. Создаем и активируем виртуальное окружение (рекомендуется для изоляции зависимостей)
# Для Windows:
python -m venv venv && venv\Scripts\activate
# Для macOS / Linux 
# python3 -m venv venv && source venv/bin/activate

### 3. Установка зависимостей

**Обязательные библиотеки:**

```bash
pip install customtkinter>=5.2.0
pip install matplotlib>=3.5.0
pip install numpy>=1.20.0
```

## 📚 Educational Value
The project clearly demonstrates:
- Why 50% of bits are discarded when bases don't match (this is normal, not an error).
- How the formula QBER = 0.25 × p + noise determines channel security.
- Why BB84 protocol loses its security without error correction and privacy amplification procedures when noise level exceeds 11%.

## 🛠 Technologies
- **GUI:** tkinter, ttk
- **Mathematics and Graphs:** numpy, matplotlib
- **Quantum Computing (optional):** qiskit
- **Cryptography:** hashlib (for entropy hashing demonstration)

## 📄 License
This project is distributed under the MIT License. See the LICENSE file for details.

##  Contributing

This project has a scientific research foundation (Research Work at Kurgan State University) and is under active development. Any help in the form of code, documentation, or scientific consultation is welcome!

If you want to contribute, please review the priority development areas formulated within this research:

## 🚀 Priority Tasks (Roadmap):

### ⚛️ Deep Qiskit Integration:
  Transition from the current probabilistic model to explicit use of state vectors, density matrices, and unitary operators for more rigorous physical modeling.

### 🌐 3D State Visualization:
  Add interactive Bloch sphere visualization to clearly demonstrate how qubit quantum states change when passing through the channel and during Eve's attack.

### 🛡️ Advanced Attack Implementation:
  Add PNS (Photon Number Splitting) attack model to demonstrate vulnerabilities of real laser sources (multi-photon pulses), as opposed to the idealized intercept-resend model.

### 🌫️ Improved Decoherence Model:
  Implement more sophisticated natural channel noise models (e.g., phase or amplitude damping channels) to make the simulator more accurately reflect limitations of real optical communication lines.

### 🔄 Support for New Protocols:
  Expand simulator functionality to work with entanglement-based protocols (e.g., E91) or the SARG04 protocol.

### 📊 Data Export:
  Add the ability to export experimental results (QBER tables, σ values) to .csv or .xlsx formats for further independent statistical analysis.

