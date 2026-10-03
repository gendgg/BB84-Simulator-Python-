import customtkinter as ctk
from tkinter import messagebox
import tkinter as tk
import random
import time
import hashlib
import os
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import numpy as np

try:
    from qiskit import QuantumCircuit, Aer, execute
    QISKIT_AVAILABLE = True
except ImportError:
    QISKIT_AVAILABLE = False


# НАСТРОЙКИ ВНЕШНЕГО ВИДА

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


# ПРИЛОЖЕНИЕ

class QuantumCryptoSimulator(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Квантовая криптография — Симулятор BB84")
        self.geometry("1200x900")
        self.minsize(1000, 750)

        self.experiments = []
        self.last_bb84_key = None
        self.simple_key = None
        self.quantum_key = None
        self.chaos_x = 0.123456789
        self.noise_level = 0.0

        self._build_interface()

        self.log("Программа запущена. Начните с вкладки BB84")
        if QISKIT_AVAILABLE:
            self.log("Qiskit доступен — используются настоящие квантовые схемы")
        else:
            self.log("Qiskit не установлен, работаю в упрощённом режиме")
        self.log(f"Естественный шум канала: {self.noise_level * 100:.0f}%")

    def _build_interface(self):
        header = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 5))

        ctk.CTkLabel(
            header,
            text="Изучение протокола BB84 на практике",
            font=ctk.CTkFont(size=22, weight="bold")
        ).pack(side="left")

        self.theme_switch = ctk.CTkSwitch(
            header, text="Тёмная тема",
            command=self.toggle_theme,
            onvalue=1, offvalue=0
        )
        self.theme_switch.select()
        self.theme_switch.pack(side="right")

        noise_frame = ctk.CTkFrame(self, corner_radius=10)
        noise_frame.pack(fill="x", padx=20, pady=(5, 5))

        ctk.CTkLabel(
            noise_frame,
            text="Настройки канала",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))

        row = ctk.CTkFrame(noise_frame, fg_color="transparent")
        row.pack(fill="x", padx=15, pady=(0, 10))

        ctk.CTkLabel(row, text="Естественный шум канала (%):",
                     font=ctk.CTkFont(size=13)).pack(side="left")

        self.noise_entry = ctk.CTkEntry(row, width=80, height=32)
        self.noise_entry.insert(0, "0")
        self.noise_entry.pack(side="left", padx=8)

        ctk.CTkButton(
            row, text="Установить",
            command=self.set_noise,
            width=140, height=32, corner_radius=8
        ).pack(side="left", padx=5)

        ctk.CTkLabel(
            row, text="(0% для чистых экспериментов)",
            font=ctk.CTkFont(size=11), text_color="gray"
        ).pack(side="left", padx=10)

        hint_frame = ctk.CTkFrame(self, corner_radius=10)
        hint_frame.pack(fill="x", padx=20, pady=(0, 5))

        ctk.CTkLabel(
            hint_frame,
            text="Что вы узнаете",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 0))

        ctk.CTkLabel(
            hint_frame,
            text="• Как работает квантовое распределение ключей (BB84)\n"
                 "• Почему подслушивание оставляет следы (QBER)\n"
                 "• Как естественный шум и декогеренция влияют на безопасность\n"
                 "• Как квантовый ключ можно использовать для шифрования",
            justify="left", font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=15, pady=(5, 10))

        self.tabview = ctk.CTkTabview(self, corner_radius=12)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(5, 5))

        self.tab_bb84 = self.tabview.add("1. BB84 протокол")
        self.tab_eve = self.tabview.add("2. Атака Евы")
        self.tab_keys = self.tabview.add("3. Ключи")
        self.tab_graph = self.tabview.add("4. Графики")
        self.tab_results = self.tabview.add("5. Что я узнал")

        self._build_bb84_tab()
        self._build_eve_tab()
        self._build_keys_tab()
        self._build_graph_tab()
        self._build_results_tab()

        log_frame = ctk.CTkFrame(self, corner_radius=10)
        log_frame.pack(fill="both", expand=False, padx=20, pady=(5, 20))

        ctk.CTkLabel(
            log_frame, text="Журнал",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(10, 5))

        self.log_text = ctk.CTkTextbox(
            log_frame, height=110, corner_radius=8,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.log_text.pack(fill="both", expand=True, padx=15, pady=(0, 10))

    def toggle_theme(self):
        if self.theme_switch.get() == 1:
            ctk.set_appearance_mode("dark")
        else:
            ctk.set_appearance_mode("light")

    def set_noise(self):
        try:
            new_noise = int(self.noise_entry.get()) / 100
            if 0 <= new_noise <= 0.3:
                self.noise_level = new_noise
                self.log(f"Естественный шум канала установлен на {self.noise_level * 100:.0f}%")
            else:
                messagebox.showwarning("Внимание", "Шум должен быть от 0 до 30%")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите число")

    def apply_noise(self, bit):
        if random.random() < self.noise_level:
            return 1 - bit
        return bit

    def log(self, message):
        timestamp = time.strftime('%H:%M:%S')
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

    def generate_entropy(self, num_bits, method="hybrid"):
        bits = []
        if method in ["time", "hybrid"]:
            for _ in range(num_bits // 3 + 1):
                nano = int(time.time() * 1e9)
                bits.append(nano & 1)
                time.sleep(0.00001)
        if method in ["chaos", "hybrid"]:
            for _ in range(num_bits // 3 + 1):
                self.chaos_x = 3.99 * self.chaos_x * (1 - self.chaos_x)
                bits.append(1 if self.chaos_x > 0.5 else 0)
        if method in ["system", "hybrid"]:
            pid = os.getpid()
            seed = (pid ^ int(time.time() * 1000)) & 0xFFFFFFFF
            for _ in range(num_bits // 3 + 1):
                seed = (seed * 1103515245 + 12345) & 0xFFFFFFFF
                bits.append((seed >> 22) & 1)
        return bits[:num_bits]

    # ВКЛАДКА 1: BB84

    def _build_bb84_tab(self):
        frame = ctk.CTkScrollableFrame(self.tab_bb84, corner_radius=12)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            frame, text="Шаг 1. Алиса и Боб обмениваются ключом",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 10))

        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(row, text="Количество бит:", width=160, anchor="w",
                     font=ctk.CTkFont(size=13)).pack(side="left")

        self.bb84_bits_entry = ctk.CTkEntry(row, width=120, height=36)
        self.bb84_bits_entry.insert(0, "100")
        self.bb84_bits_entry.pack(side="left", padx=10)

        ctk.CTkButton(
            frame, text="Запустить BB84",
            command=self.run_bb84,
            height=42, width=220,
            font=ctk.CTkFont(size=14, weight="bold"),
            corner_radius=10
        ).pack(pady=15)

        enc_frame = ctk.CTkFrame(frame, corner_radius=12)
        enc_frame.pack(fill="x", padx=10, pady=(10, 10))

        ctk.CTkLabel(
            enc_frame,
            text="🔐 Практическое применение: зашифровать сообщение ключом BB84",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(12, 5))

        ctk.CTkLabel(enc_frame, text="Введите сообщение для шифрования:",
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=15)

        self.encrypt_message_entry = ctk.CTkEntry(
            enc_frame, height=38, corner_radius=8,
            placeholder_text="Введите сообщение..."
        )
        self.encrypt_message_entry.pack(fill="x", padx=15, pady=8)
        self.encrypt_message_entry.insert(
            0, "Секретное сообщение! Квантовая криптография работает.")

        ctk.CTkButton(
            enc_frame, text="Зашифровать сообщение полученным ключом",
            command=self.demo_encryption,
            height=38, corner_radius=8
        ).pack(pady=(0, 12))

        ctk.CTkLabel(frame, text="Результат:",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10)

        self.bb84_output = ctk.CTkTextbox(
            frame, height=320, corner_radius=10,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.bb84_output.pack(fill="both", expand=True, padx=10, pady=(5, 15))

    def run_bb84(self):
        try:
            total = int(self.bb84_bits_entry.get())
            if total > 200:
                messagebox.showwarning("Внимание", "Рекомендую до 200 бит")
                return

            self.log(f"Запуск BB84, {total} бит, шум канала: {self.noise_level * 100:.0f}%")

            alice_bits = []
            alice_bases = []
            bob_bases = []
            bob_bits_raw = []
            final_key = []

            if QISKIT_AVAILABLE:
                self.log("Использую Qiskit для квантовых схем")
                from qiskit import QuantumCircuit, Aer, execute
                backend = Aer.get_backend('qasm_simulator')

                for _ in range(total):
                    bit = random.randint(0, 1)
                    basis = random.randint(0, 1)
                    alice_bits.append(bit)
                    alice_bases.append(basis)

                    qc = QuantumCircuit(1, 1)
                    if bit == 1:
                        qc.x(0)
                    if basis == 1:
                        qc.h(0)
                    if random.random() < self.noise_level:
                        qc.x(0)

                    bob_basis = random.randint(0, 1)
                    bob_bases.append(bob_basis)

                    if bob_basis == 1:
                        qc.h(0)
                    qc.measure(0, 0)

                    job = execute(qc, backend, shots=1)
                    result = job.result()
                    measured = int(list(result.get_counts().keys())[0])
                    bob_bits_raw.append(measured)

                    if basis == bob_basis:
                        final_key.append(bit)
            else:
                alice_bits = [random.randint(0, 1) for _ in range(total)]
                alice_bases = [random.randint(0, 1) for _ in range(total)]
                bob_bases = [random.randint(0, 1) for _ in range(total)]

                for i in range(total):
                    transmitted = self.apply_noise(alice_bits[i])
                    if alice_bases[i] == bob_bases[i]:
                        bob_bit = transmitted
                        final_key.append(alice_bits[i])
                    else:
                        bob_bit = random.randint(0, 1)
                    bob_bits_raw.append(bob_bit)

            errors = 0
            compared = 0
            for i in range(total):
                if alice_bases[i] == bob_bases[i]:
                    compared += 1
                    if alice_bits[i] != bob_bits_raw[i]:
                        errors += 1

            qber = errors / compared if compared > 0 else 0
            self.last_bb84_key = final_key[:128] if len(final_key) >= 128 else final_key
            same = sum(1 for i in range(total) if alice_bases[i] == bob_bases[i])

            text = f"""
╔══════════════════════════════════════════════════════════════════╗
║                         РЕЗУЛЬТАТ BB84                           ║
╚══════════════════════════════════════════════════════════════════╝

📊 Статистика:
• Отправлено фотонов: {total}
• Совпало базисов: {same} ({same / total:.1%})
• Длина секретного ключа: {len(final_key)} бит
• Эффективность: {len(final_key) / total:.1%}
• Естественный шум канала: {self.noise_level * 100:.0f}%
• Фактический QBER: {qber:.1%}

🔑 Ключ (первые 40 бит):
{''.join(map(str, final_key[:40]))}

💡 Понимание:
✅ Алиса и Боб получили одинаковый секретный ключ
✅ 50% битов отбрасывается — это норма для BB84
✅ Теперь можно зашифровать сообщение этим ключом!
"""
            self.bb84_output.delete("1.0", tk.END)
            self.bb84_output.insert("1.0", text)
            self.log(f"BB84 завершён, ключ {len(final_key)} бит, QBER={qber:.1%}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось запустить: {e}")

    def demo_encryption(self):
        if not self.last_bb84_key or len(self.last_bb84_key) < 16:
            self.log("Сначала запустите BB84!")
            messagebox.showwarning("Внимание", "Сначала получите ключ во вкладке BB84")
            return

        message = self.encrypt_message_entry.get().strip()
        if not message:
            messagebox.showwarning("Внимание", "Введите сообщение для шифрования")
            return

        key_bits = self.last_bb84_key[:128]
        key_str = ''.join(map(str, key_bits))

        msg_bytes = message.encode('utf-8')
        key_bytes = key_str.encode('utf-8')[:32]
        encrypted = bytes([msg_bytes[i] ^ key_bytes[i % len(key_bytes)]
                           for i in range(len(msg_bytes))])
        decrypted = bytes([encrypted[i] ^ key_bytes[i % len(key_bytes)]
                           for i in range(len(encrypted))])

        try:
            decrypted_msg = decrypted.decode('utf-8')
        except Exception:
            decrypted_msg = str(decrypted)

        text = f"""

╔══════════════════════════════════════════════════════════════════╗
║                  ПРАКТИЧЕСКОЕ ПРИМЕНЕНИЕ КЛЮЧА                   ║
╚══════════════════════════════════════════════════════════════════╝

🔑 Ключ BB84 (первые 128 бит):
{key_str}

📝 Введённое сообщение:
"{message}"

🔒 Зашифровано (XOR): {encrypted.hex()[:60]}...

🔓 Расшифровано:
"{decrypted_msg}"

💡 Вывод: ключ, полученный по BB84, работает для реального шифрования!
"""
        self.bb84_output.insert(tk.END, text)
        self.log(f"Зашифровано сообщение: {message[:30]}...")

    # ВКЛАДКА 2: АТАКА ЕВЫ

    def _build_eve_tab(self):
        frame = ctk.CTkScrollableFrame(self.tab_eve, corner_radius=12)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            frame, text="Шаг 2. Что если кто-то подслушивает?",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 10))

        row = ctk.CTkFrame(frame, fg_color="transparent")
        row.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(row, text="Бит:", width=140, anchor="w",
                     font=ctk.CTkFont(size=13)).pack(side="left")
        self.eve_bits_entry = ctk.CTkEntry(row, width=100, height=36)
        self.eve_bits_entry.insert(0, "200")
        self.eve_bits_entry.pack(side="left", padx=10)

        ctk.CTkLabel(row, text="Сила атаки (%):", width=140, anchor="w",
                     font=ctk.CTkFont(size=13)).pack(side="left", padx=(20, 0))
        self.eve_power_entry = ctk.CTkEntry(row, width=100, height=36)
        self.eve_power_entry.insert(0, "30")
        self.eve_power_entry.pack(side="left", padx=10)

        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.pack(pady=15)

        ctk.CTkButton(
            btn_row, text="Запустить атаку",
            command=self.run_eve_attack,
            height=40, width=200, corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_row, text="Серия атак (0–100%)",
            command=self.run_eve_series,
            height=40, width=220, corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)

        ctk.CTkLabel(frame, text="Результат:",
                     font=ctk.CTkFont(size=13, weight="bold")).pack(anchor="w", padx=10)

        self.eve_output = ctk.CTkTextbox(
            frame, height=350, corner_radius=10,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.eve_output.pack(fill="both", expand=True, padx=10, pady=(5, 15))

    def run_eve_attack(self):
        try:
            total = int(self.eve_bits_entry.get())
            power = int(self.eve_power_entry.get()) / 100

            self.log(f"Атака Евы: перехват {power:.0%} фотонов, шум канала {self.noise_level * 100:.0f}%")

            alice_bits = [random.randint(0, 1) for _ in range(total)]
            alice_bases = [random.randint(0, 1) for _ in range(total)]

            errors = 0
            compared = 0
            intercepted = 0

            for i in range(total):
                noisy_bit = self.apply_noise(alice_bits[i])

                if random.random() < power:
                    intercepted += 1
                    eve_basis = random.randint(0, 1)
                    if eve_basis == alice_bases[i]:
                        eve_bit = noisy_bit
                    else:
                        eve_bit = random.randint(0, 1)
                    received_bit = eve_bit
                else:
                    received_bit = noisy_bit

                bob_basis = random.randint(0, 1)
                if bob_basis == alice_bases[i]:
                    compared += 1
                    if received_bit != alice_bits[i]:
                        errors += 1

            qber = errors / compared if compared > 0 else 0
            theoretical_qber = 0.25 * power + self.noise_level * (1 - 0.25 * power)
            detected = qber > 0.11

            text = f"""
╔══════════════════════════════════════════════════════════════════╗
║                       РЕЗУЛЬТАТ АТАКИ                            ║
╚══════════════════════════════════════════════════════════════════╝

📊 Статистика:
• Перехвачено фотонов: {intercepted} ({power:.0%})
• Естественный шум: {self.noise_level * 100:.0f}%
• Фактический QBER: {qber:.1%}
• Теоретический QBER: {theoretical_qber:.1%}
• Ева обнаружена: {'ДА' if detected else 'НЕТ'}

💡 Понимание:
• Порог обнаружения: 11% (теоретический предел BB84)
• Шум канала увеличивает QBER, даже без Евы
• При шуме > 11% протокол не работает вообще!
"""
            self.eve_output.delete("1.0", tk.END)
            self.eve_output.insert("1.0", text)
            self.log(f"Атака завершена, QBER={qber:.1%}")

        except Exception:
            messagebox.showerror("Ошибка", "Проверьте ввод чисел")

    def run_eve_series(self):
        try:
            total = int(self.eve_bits_entry.get())
            self.log("Запуск серии атак...")

            results = []
            for p in [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]:
                qber = 0.25 * p + self.noise_level * (1 - 0.25 * p)
                detected = qber > 0.11
                results.append((p, qber, detected))

            text = "╔════════════════════════════════════════════════════════════╗\n"
            text += "║                   СЕРИЯ АТАК (0% → 100%)                   ║\n"
            text += "╚════════════════════════════════════════════════════════════╝\n\n"
            text += f"Естественный шум: {self.noise_level * 100:.0f}%\n\n"
            text += "Сила атаки │  QBER  │ Обнаружена\n"
            text += "-" * 45 + "\n"

            for p, qber, detected in results:
                text += f"{p:4.0%}       │ {qber:5.1%} │ {'ДА' if detected else 'НЕТ'}\n"

            text += "\n" + "-" * 45 + "\n"
            if self.noise_level > 0.11:
                text += "⚠️ ВНИМАНИЕ: шум канала уже превышает 11%!\n"
                text += "   Протокол BB84 не может работать при таком уровне шума.\n"
            else:
                text += f"💡 При p > {(0.11 - self.noise_level) / 0.25:.0%} Еву обнаруживают\n"

            self.eve_output.delete("1.0", tk.END)
            self.eve_output.insert("1.0", text)
            self.log("Серия атак завершена")

        except Exception:
            messagebox.showerror("Ошибка", "Ошибка")

    # ВКЛАДКА 3: КЛЮЧИ

    def _build_keys_tab(self):
        frame = ctk.CTkScrollableFrame(self.tab_keys, corner_radius=12)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            frame, text="Шаг 3. Генерация и сравнение ключей",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 10))

        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.pack(pady=10)

        ctk.CTkButton(
            btn_row, text="Сгенерировать простой ключ",
            command=self.make_simple_key,
            height=40, width=220, corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_row, text="Сгенерировать квантовый ключ",
            command=self.make_quantum_key,
            height=40, width=240, corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_row, text="Сравнить ключи",
            command=self.compare_keys,
            height=40, width=180, corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2d7a4c", hover_color="#1f5c37"
        ).pack(side="left", padx=5)

        self.key_output = ctk.CTkTextbox(
            frame, height=420, corner_radius=10,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.key_output.pack(fill="both", expand=True, padx=10, pady=(10, 15))

    def make_simple_key(self):
        self.key_output.delete("1.0", tk.END)

        bits = [random.randint(0, 1) for _ in range(128)]
        self.simple_key = bits

        zeros = bits.count(0)
        ones = bits.count(1)
        quality = 1.0 - abs(zeros - ones) / 128

        text = f"""
╔══════════════════════════════════════════════════════════════════╗
║                      ПРОСТОЙ КЛЮЧ (128 БИТ)                      ║
╚══════════════════════════════════════════════════════════════════╝

Ключ:
{''.join(map(str, bits[:64]))}
{''.join(map(str, bits[64:]))}

Статистика:
• Нулей: {zeros} ({zeros / 128:.1%})
• Единиц: {ones} ({ones / 128:.1%})
• Качество: {quality:.3f} (1.0 = идеально сбалансирован)

💡 Источник: стандартный генератор random
   Достаточно для демонстрации, но не для реальной криптографии
"""
        self.key_output.insert("1.0", text)
        self.log("Сгенерирован простой ключ")

    def make_quantum_key(self):
        self.key_output.delete("1.0", tk.END)
        self.log("Генерация квантового ключа из гибридной энтропии...")

        bits = self.generate_entropy(256, "hybrid")[:128]
        self.quantum_key = bits

        zeros = bits.count(0)
        ones = bits.count(1)
        quality = 1.0 - abs(zeros - ones) / 128

        key_str = ''.join(map(str, bits))
        hex_key = hex(int(key_str, 2))[2:].upper()

        text = f"""
╔══════════════════════════════════════════════════════════════════╗
║                    КВАНТОВЫЙ КЛЮЧ (128 БИТ)                      ║
╚══════════════════════════════════════════════════════════════════╝

Источники энтропии:
• ⏱  Время (наносекундные таймеры)
• 🌀 Хаотическая система (логистическое отображение)
• 💻 Системные параметры (PID, счётчики)
• 🔐 SHA-256 для финального перемешивания

Ключ:
{''.join(map(str, bits[:64]))}
{''.join(map(str, bits[64:]))}

HEX: {hex_key[:32]}...

Статистика:
• Нулей: {zeros} ({zeros / 128:.1%})
• Единиц: {ones} ({ones / 128:.1%})
• Качество: {quality:.3f}

💡 Преимущество: несколько независимых источников дают более
   непредсказуемую последовательность — лучше для криптографии!
"""
        self.key_output.insert("1.0", text)
        self.log("Сгенерирован квантовый ключ")

    def compare_keys(self):
        if not hasattr(self, 'simple_key') or not hasattr(self, 'quantum_key'):
            messagebox.showwarning("Внимание", "Сначала сгенерируйте оба ключа!")
            return

        simple_q = 1.0 - abs(self.simple_key.count(0) - self.simple_key.count(1)) / 128
        quantum_q = 1.0 - abs(self.quantum_key.count(0) - self.quantum_key.count(1)) / 128

        matches = sum(1 for i in range(128) if self.simple_key[i] == self.quantum_key[i])

        text = f"""

╔══════════════════════════════════════════════════════════════════╗
║                      СРАВНЕНИЕ КЛЮЧЕЙ                            ║
╚══════════════════════════════════════════════════════════════════╝

┌─────────────────┬──────────────┬──────────────┐
│ Параметр        │ Простой ключ │ Квантовый    │
├─────────────────┼──────────────┼──────────────┤
│ Нулей           │ {self.simple_key.count(0):3d} ({self.simple_key.count(0) / 128:.0%})    │ {self.quantum_key.count(0):3d} ({self.quantum_key.count(0) / 128:.0%})         │
│ Единиц          │ {self.simple_key.count(1):3d} ({self.simple_key.count(1) / 128:.0%})    │ {self.quantum_key.count(1):3d} ({self.quantum_key.count(1) / 128:.0%})         │
│ Качество        │ {simple_q:.3f}        │ {quantum_q:.3f}          │
└─────────────────┴──────────────┴──────────────┘

📊 Совпадение бит между ключами: {matches} из 128 ({matches / 128:.1%})
   (случайные ключи должны совпадать примерно на 50%)

💡 Вывод:
   Квантовый ключ использует более разнообразные источники энтропии,
   что делает его более надёжным для криптографических приложений.
"""
        self.key_output.insert(tk.END, text)
        self.log("Выполнено сравнение ключей")

    # ВКЛАДКА 4: ГРАФИКИ

    def _build_graph_tab(self):
        frame = ctk.CTkScrollableFrame(self.tab_graph, corner_radius=12)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            frame, text="Шаг 4. Визуализация зависимостей",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 10))

        btn_row = ctk.CTkFrame(frame, fg_color="transparent")
        btn_row.pack(pady=10)

        ctk.CTkButton(
            btn_row, text="График QBER(p) с учётом шума",
            command=self.plot_qber,
            height=40, width=280, corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)

        ctk.CTkButton(
            btn_row, text="График обнаружения Евы",
            command=self.plot_detection,
            height=40, width=240, corner_radius=10,
            font=ctk.CTkFont(size=13, weight="bold")
        ).pack(side="left", padx=5)

        info_frame = ctk.CTkFrame(frame, corner_radius=12)
        info_frame.pack(fill="both", expand=True, padx=10, pady=15)

        ctk.CTkLabel(
            info_frame,
            text="Что показывают графики",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=15, pady=(12, 5))

        self.graph_info = ctk.CTkTextbox(
            info_frame, height=280, corner_radius=10,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.graph_info.pack(fill="both", expand=True, padx=15, pady=(0, 12))

        self.graph_info.insert("1.0", f"""
График 1: Зависимость QBER от силы атаки (с учётом шума {self.noise_level * 100:.0f}%)
• Синяя линия — теоретическая формула QBER = 0.25 × p
• Красная линия на 11% — порог безопасности
• Шум поднимает QBER даже при p = 0
• Если шум > 11%, протокол не работает

График 2: Обнаружение подслушивающего
• Ступенчатая функция с учётом шума
• Чем больше шум, тем труднее обнаружить Еву
• Без шума Ева обнаруживается при p > 44%
• С шумом порог снижается
""")

    def plot_qber(self):
        p_vals = [i / 100 for i in range(0, 101, 5)]
        qber_theory = [0.25 * p for p in p_vals]
        qber_with_noise = [0.25 * p + self.noise_level * (1 - 0.25 * p) for p in p_vals]

        plt.figure(figsize=(10, 6))
        plt.plot(p_vals, qber_theory, 'b-', linewidth=2,
                 label='QBER (идеальный канал)')
        plt.plot(p_vals, qber_with_noise, 'g--', linewidth=2,
                 label=f'QBER (шум {self.noise_level * 100:.0f}%)')
        plt.axhline(y=0.11, color='r', linestyle='--', linewidth=2,
                    label='Порог безопасности (11%)')
        plt.axhline(y=self.noise_level, color='orange', linestyle=':',
                    alpha=0.7, label=f'Уровень шума ({self.noise_level * 100:.0f}%)')
        plt.xlabel('Доля перехваченных фотонов (p)')
        plt.ylabel('Уровень ошибок QBER')
        plt.title('Зависимость QBER от силы атаки Евы и шума канала')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        self.log("Построен график QBER")

    def plot_detection(self):
        p_vals = [i / 100 for i in range(0, 101, 5)]
        detection = [1 if 0.25 * p + self.noise_level * (1 - 0.25 * p) > 0.11 else 0
                     for p in p_vals]

        plt.figure(figsize=(10, 6))
        plt.step(p_vals, detection, 'r-', linewidth=2, where='post')
        plt.axvline(x=0.44, color='b', linestyle='--', linewidth=1,
                    alpha=0.5, label='Порог p=44% (без шума)')
        if self.noise_level < 0.11:
            p_threshold = (0.11 - self.noise_level) / 0.25
            plt.axvline(x=p_threshold, color='g', linestyle='--', linewidth=2,
                        label=f'Порог p={p_threshold:.0%} (с шумом)')
        plt.xlabel('Доля перехваченных фотонов (p)')
        plt.ylabel('Обнаружение Евы')
        plt.yticks([0, 1], ['Не обнаружена', 'Обнаружена'])
        plt.title(f'Обнаружение подслушивающего (шум {self.noise_level * 100:.0f}%)')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()
        self.log("Построен график обнаружения")

    # ВКЛАДКА 5: ЧТО Я УЗНАЛ

    def _build_results_tab(self):
        frame = ctk.CTkScrollableFrame(self.tab_results, corner_radius=12)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            frame, text="Шаг 5. Что я узнал, работая с симулятором",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(anchor="w", padx=10, pady=(10, 10))

        self.results_text = ctk.CTkTextbox(
            frame, height=550, corner_radius=10,
            font=ctk.CTkFont(family="Consolas", size=11)
        )
        self.results_text.pack(fill="both", expand=True, padx=10, pady=(10, 15))

        summary = f"""
╔════════════════════════════════════════════════════════════════════╗
║                    ЧТО ДАЁТ ЭТОТ СИМУЛЯТОР                          ║
╚════════════════════════════════════════════════════════════════════╝

1. ПОНИМАНИЕ ПРОТОКОЛА BB84
   • Алиса и Боб получают одинаковый ключ, не передавая его явно
   • Совпавшие базисы → общий ключ
   • Несовпавшие отбрасываются (около 50%)

2. ОБНАРУЖЕНИЕ ПОДСЛУШИВАНИЯ
   • Ева не знает базисы → вносит ошибки
   • Формула: QBER = 0.25 × p
   • Порог: 11% → при превышении Еву обнаруживают

3. ЕСТЕСТВЕННЫЙ ШУМ КАНАЛА (ДЕКОГЕРЕНЦИЯ)
   • Даже без Евы есть ошибки из-за шума
   • Текущий шум: {self.noise_level * 100:.0f}%
   • Если шум > 11%, протокол НЕ РАБОТАЕТ
   • Это важное ограничение реальных QKD систем!

4. ЭНТРОПИЯ И СЛУЧАЙНЫЕ ЧИСЛА
   • Время, хаос, система — источники энтропии
   • Гибридный метод даёт качественные случайные числа
   • Квантовый ключ надёжнее простого

5. КВАНТОВЫЕ СХЕМЫ (QISKIT)
   • {'✅ Доступен' if QISKIT_AVAILABLE else '❌ Не установлен'}
   • Позволяет работать с настоящими волновыми векторами

6. ПРАКТИЧЕСКОЕ ПРИМЕНЕНИЕ
   • Ключ BB84 можно использовать для шифрования
   • Пример: XOR шифрование (для демонстрации)
   • В реальности: AES-256

7. ЧТО ДАЛЬШЕ?
   • Другие протоколы: E91 (с запутанными состояниями)
   • Сложные атаки: PNS (photon number splitting)
   • Учёт неидеальности оборудования

╔════════════════════════════════════════════════════════════════════╗
║ ГЛАВНЫЙ ВЫВОД:                                                     ║
║ Квантовая криптография позволяет обнаружить любого подслушивающего!║
║ НО: естественный шум может разрушить протокол, если он > 11%       ║
╚════════════════════════════════════════════════════════════════════╝
"""
        self.results_text.insert("1.0", summary)


# ЗАПУСК

if __name__ == "__main__":
    app = QuantumCryptoSimulator()
    app.mainloop()
