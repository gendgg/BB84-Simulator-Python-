## 🔐 Квантовый криптографический симулятор BB84 / BB84 Quantum Cryptography Simulator

Интерактивный образовательный симулятор протокола квантового распределения ключей BB84 с графическим интерфейсом. Проект предназначен для изучения основ квантовой криптографии, влияния шума канала (декогеренции) и атак перехвата (Eve's attack) на безопасность связи.

An interactive educational simulator of the BB84 quantum key distribution protocol with a graphical user interface. Designed to study the fundamentals of quantum cryptography, the impact of channel noise (decoherence), and interception attacks (Eve's attack) on communication security.

![Python](https://img.shields.io/badge/Python-3.13+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Qiskit](https://img.shields.io/badge/Qiskit-Optional-purple.svg)
![CustomTkinter](https://img.shields.io/badge/CustomTkinter-5.2.2-blueviolet.svg)

## 📸 Описание вкладок / Description of the inserts
 1. Вкладка BB84 /  BB84 Tab:
    Базовый обмен ключом без атаки. Показывает генерацию битов, выбор базисов, отбрасывание ~50%, формирование ключа. Плюс шифрование сообщения полученным ключом.
    (Basic key exchange without an attack. Shows bit generation, basis selection, discarding ~50%, key formation. Plus encryption of the message using the obtained key.)
   <img width="1823" height="1080" alt="image" src="https://github.com/user-attachments/assets/64d5f03e-aad6-4a67-8212-e9000b286afc" />

 2. Атака Евы / Eve's Attack:
    Intercept-resend атака. Настройка силы атаки (0–100%) и шума канала (0–30%). Расчёт QBER, автоматическое обнаружение Евы при QBER > 11%.
    (Intercept-resend attack. Attack strength setting (0–100%) and channel noise (0–30%). QBER calculation, automatic detection of Eve when QBER > 11%.)
   <img width="1825" height="1080" alt="image" src="https://github.com/user-attachments/assets/8476106f-6477-4a64-9d62-ed5f979f6adc" />

 3. Генерация и сравнение ключей / Key Generation and Comparison:
    Сравнение простого и квантового ключа. Метрика качества — сбалансированность нулей и единиц.
    (Comparison of a simple and a quantum key. Quality metric — balance of zeros and ones.)
   <img width="1824" height="1080" alt="image" src="https://github.com/user-attachments/assets/061a2af5-9c33-4ecd-b29b-05d416a82b46" />

 4. Графики / Graphs:
    Зависимость QBER(p) и ступенчатая функция обнаружения Евы.
    (The dependence QBER(p) and the step function of Eve’s detection.)
   <img width="1823" height="1080" alt="image" src="https://github.com/user-attachments/assets/101a3c8b-bee6-48b3-9dca-735f68036c32" />

 5. Результаты измерений и соответствующие им выводы /  Measurement Results and Conclusions:
    Сводная таблица, регрессионный анализ, статистическая проверка, выводы.
    (Summary table, regression analysis, statistical testing, conclusions.)
   <img width="1822" height="1080" alt="image" src="https://github.com/user-attachments/assets/915ef163-2937-434e-973b-9f13f5afb05d" />


## ✨ Возможности / Features

- **Симуляция протокола BB84:** Генерация квантового ключа с учетом выбора базисов Алисой и Бобом.  
  *(BB84 Protocol Simulation: Quantum key generation accounting for Alice and Bob's basis choices.)*

- **Моделирование шума канала:** Настройка уровня естественного шума (декогеренции) и наблюдение за его влиянием на QBER (Quantum Bit Error Rate).  
  *(Channel Noise Modeling: Configurable natural noise (decoherence) level with observation of its impact on QBER — Quantum Bit Error Rate.)*

- **Атака Евы:** Визуализация перехвата фотонов и демонстрация того, почему подслушивание в квантовой криптографии всегда оставляет следы (порог обнаружения ~11%).  
  *(Eve's Attack: Visualization of photon interception demonstrating why eavesdropping in quantum cryptography always leaves traces — detection threshold ~11%.)*

- **Генерация энтропии:** Сравнение простого генератора случайных чисел с гибридным методом (время, хаотические системы, системные параметры).  
  *(Entropy Generation: Comparison of a simple random number generator with a hybrid method — time, chaotic systems, system parameters.)*

- **Визуализация:** Построение графиков зависимости QBER от силы атаки с использованием `matplotlib`.  
  *(Visualization: Plotting QBER dependence on attack strength using `matplotlib`.)*

- **Поддержка Qiskit:** Если установлена библиотека Qiskit, симуляция использует реальные квантовые схемы (волновые векторы), иначе работает в упрощенном вероятностном режиме.  
  *(Qiskit Support: If the Qiskit library is installed, the simulation uses real quantum circuits (state vectors); otherwise it operates in a simplified probabilistic mode.)*

## 🚀 Установка и запуск / Installation and Launch

### 1. Клонирование репозитория / Clone the repository

```bash
git clone https://github.com/gendgg/project.git
cd project
```

### 2. Создание виртуального окружения / Create a virtual environmen

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей / Install dependencies

**Обязательные библиотеки:**

```bash
pip install customtkinter>=5.2.0
pip install matplotlib>=3.5.0
pip install numpy>=1.20.0
```

**Опционально — Qiskit:**

```bash
pip install qiskit qiskit-aer
```

### 4. Запуск / Launch

```bash
python bb84.py
```

## 🎨 Установка CustomTkinter / CustomTkinter Installation

Проект использует **CustomTkinter** — библиотеку для современных GUI. Она **не входит** в стандартную поставку Python.

### Установка / Installation

```bash
pip install customtkinter
```

### Если несколько версий Python / If you have multiple Python versions

```bash
py -3.13 -m pip install customtkinter
```

### Проверка / Verification

```bash
python -c "import customtkinter; print(customtkinter.__version__)"
```

Должно вывести версию, например `5.2.2`.

### Возможные проблемы / Possible Issues

| Проблема | Решение |
|----------|---------|
| `ModuleNotFoundError: No module named 'customtkinter'` | Библиотека в другом Python — проверьте интерпретатор |
| `pip: command not found` | Запустите `python -m ensurepip --upgrade` |
| Окно не появляется | Версия 6.0.0 может быть несовместима с Python 3.13 — используйте 5.2.2 |
| IDE не видит библиотеку | Установите через настройки IDE (PyCharm: File → Settings → Python Interpreter) |

### Рекомендуемая версия / Recommended Version

```bash
pip install customtkinter==5.2.2
```

## 💻 Системные требования / System Requirements

**Минимальные / Minimum:**
- Python 3.8+
- 4 ГБ ОЗУ
- 200 МБ свободного места

**Рекомендуемые / Recommended:**
- Python 3.10–3.13
- 8 ГБ ОЗУ
- 500 МБ (с Qiskit)

**Обязательные зависимости / Required dependencies:**
- customtkinter >= 5.2.0
- matplotlib >= 3.5.0
- numpy >= 1.20.0

**Опциональные / Optional:**
- qiskit >= 0.40.0
- qiskit-aer >= 0.12.0

**Протестировано на / Tested on:**
- Windows 10
- 16 ГБ ОЗУ
- Ndivia RTX 2060
- AMD Ryzen 5 7000 Series
- Python 3.13.7
- CustomTkinter 5.2.2
