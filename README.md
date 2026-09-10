=== RUS ===

## 🔐 Квантовый криптографический симулятор BB84

Интерактивный образовательный симулятор протокола квантового распределения ключей BB84 с графическим интерфейсом. Проект предназначен для изучения основ квантовой криптографии, влияния шума канала (декогеренции) и атак перехвата (Eve's attack) на безопасность связи.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Qiskit](https://img.shields.io/badge/Qiskit-Optional-purple.svg)

## 📸 Скриншоты
 1. Вкладка BB84:
   <img width="1247" height="1079" alt="image" src="https://github.com/user-attachments/assets/c7e0025f-ca8a-4cd5-8570-a3f7c33d3ebc" />
 2. Атака Евы:
   <img width="1247" height="1076" alt="image" src="https://github.com/user-attachments/assets/5bc8c3b2-89ce-4dcb-b553-c088c94cd587" />
 3. Генерация и сравнение ключей:
   <img width="1247" height="1075" alt="image" src="https://github.com/user-attachments/assets/bb1bc241-0bbf-4cd9-bbd1-50b4156193ef" />
 4. Графики:
   <img width="1247" height="1079" alt="image" src="https://github.com/user-attachments/assets/4ed1427f-465b-48e9-8d49-f9c3210aff0b" />
 5. Результаты измерений и соответствующие им выводы:
   <img width="1250" height="1079" alt="image" src="https://github.com/user-attachments/assets/0a87da2f-a2e6-42d2-bac4-55545b7c92f4" />

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

# 3. Устанавливаем все необходимые библиотеки из файла requirements.txt
pip install -r requirements.txt

# 4. Устанавливаем Qiskit для полноценной работы с квантовыми схемами, а не в упрощенном режиме
pip install qiskit qiskit-aer

# 5. Запускаем приложение 
python bb84.py

## 📚 Образовательная ценность
Проект наглядно демонстрирует:
Почему 50% битов отбрасываются при несовпадении базисов (это норма, а не ошибка).
Как формула QBER = 0.25 × p + шум определяет безопасность канала.
Почему при уровне шума > 11% протокол BB84 теряет свою безопасность без процедур исправления ошибок и усиления приватности.

## 🛠 Технологии
GUI: tkinter, ttk
Математика и графики: numpy, matplotlib
Квантовые вычисления (опционально): qiskit
Криптография: hashlib (для демонстрации хеширования энтропии)

## 📄 Лицензия
Этот проект распространяется под лицензией MIT. Подробности в файле LICENSE.

## 🤝 Вклад в проект

Этот проект имеет научно-исследовательскую базу (НИР Курганского государственного университета) и находится в стадии активного развития. Любая помощь в виде кода, документации или научных консультаций приветствуется!
Если вы хотите внести свой вклад, ознакомьтесь с приоритетными направлениями развития, сформулированными в рамках данного исследования:
## 🚀 Приоритетные задачи (Roadmap):

# ⚛️ Глубокая интеграция с Qiskit: 
  Перевод текущей вероятностной модели на явное использование волновых векторов, матриц плотности и унитарных операторов для более строгого физического моделирования.
# 🌐 3D-визуализация состояний: 
  Добавление интерактивного отображения сферы Блоха для наглядной демонстрации того, как меняются квантовые состояния кубитов при прохождении через канал и при атаке Евы.
# 🛡️ Реализация сложных атак: 
  Добавление модели атаки PNS (Photon Number Splitting) для демонстрации уязвимостей реальных лазерных источников (многофотонных импульсов), в отличие от идеализированной модели intercept-resend.
# 🌫️ Улучшенная модель декогеренции: 
  Внедрение более сложных моделей естественного шума канала (например, фазовая или амплитудная демпфирующая среда), чтобы симулятор точнее отражал ограничения реальных оптических линий связи.
# 🔄 Поддержка новых протоколов: 
  Расширение функционала симулятора для работы с протоколами на запутанных состояниях (например, E91) или протоколом SARG04.
# 📊 Экспорт данных: 
  Добавление возможности выгрузки результатов экспериментов (таблиц QBER, значений σ) в форматы .csv или .xlsx для дальнейшей независимой статистической обработки.

=== ENG ===

## 🔐 BB84 Quantum Cryptography Simulator

An interactive educational simulator for the BB84 quantum key distribution protocol with a graphical user interface. This project is designed to study the fundamentals of quantum cryptography, the impact of channel noise (decoherence), and interception attacks (Eve's attack) on communication security.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Qiskit](https://img.shields.io/badge/Qiskit-Optional-purple.svg)

## 📸 Screenshots
 1. BB84 Tab:
   <img width="1247" height="1079" alt="image" src="https://github.com/user-attachments/assets/c7e0025f-ca8a-4cd5-8570-a3f7c33d3ebc" />
 2. Eve's Attack:
   <img width="1247" height="1076" alt="image" src="https://github.com/user-attachments/assets/5bc8c3b2-89ce-4dcb-b553-c088c94cd587" />
 3. Key Generation and Comparison:
   <img width="1247" height="1075" alt="image" src="https://github.com/user-attachments/assets/bb1bc241-0bbf-4cd9-bbd1-50b4156193ef" />
 4. Graphs:
   <img width="1247" height="1079" alt="image" src="https://github.com/user-attachments/assets/4ed1427f-465b-48e9-8d49-f9c3210aff0b" />
 5. Measurement Results and Conclusions:
   <img width="1250" height="1079" alt="image" src="https://github.com/user-attachments/assets/0a87da2f-a2e6-42d2-bac4-55545b7c92f4" />

##  Features
- **BB84 Protocol Simulation:** Quantum key generation accounting for Alice and Bob's basis choices.
- **Channel Noise Modeling:** Configurable natural noise (decoherence) level with observation of its impact on QBER (Quantum Bit Error Rate).
- **Eve's Attack:** Visualization of photon interception demonstrating why eavesdropping in quantum cryptography always leaves traces (detection threshold ~11%).
- **Entropy Generation:** Comparison of a simple random number generator with a hybrid method (time, chaotic systems, system parameters).
- **Visualization:** Plotting QBER dependence on attack strength using `matplotlib`.
- **Qiskit Support:** If the Qiskit library is installed, the simulation uses real quantum circuits (state vectors); otherwise, it operates in a simplified probabilistic mode.

## 🚀 Installation and Launch

```bash
# 1. Clone the repository and navigate to its folder
git clone https://github.com/gendgg/project.git
cd project

# 2. Create and activate a virtual environment (recommended for dependency isolation)
# For Windows:
python -m venv venv && venv\Scripts\activate
# For macOS / Linux:
# python3 -m venv venv && source venv/bin/activate

# 3. Install all required libraries from requirements.txt
pip install -r requirements.txt

# 4. Install Qiskit for full quantum circuit functionality (not just simplified mode)
pip install qiskit qiskit-aer

# 5. Launch the application
python bb84.py
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

