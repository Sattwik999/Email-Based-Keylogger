# Email-Based Keylogger

Hi! I'm Sattwik Sarkar, and this is **Email-Based Keylogger**—a Python project demonstrating simple keylogging techniques with email-based reporting. This project is strictly for educational and demonstration purposes and should never be used with malicious intent.

---

## 🚀 Project Overview

The Email-Based Keylogger runs in the background, captures keystrokes, and periodically sends the logs to a configured email address. You can use this project to understand:

- Keyboard event capturing in Python
- File handling and log management
- Secure email transmission (SMTP)
- Automation & scheduling (timed email reports)

> **Note:** Always use responsibly and only on systems you own or have explicit permission for. This tool is for learning, not for unethical use.

---

## 🧠 Logic & Working

**How the Keylogger Works:**

1. **GUI & User Control:**  
   The project provides a simple graphical user interface (GUI) using Tkinter and ttkbootstrap (main keylogger), and PyQt5 (detector utility).  
   - You can start/stop logging, view logs, save them, or clear them with a button.

2. **Key Event Capture:**  
   The app uses `pynput` to listen for keyboard events.  
   - Every keystroke is logged and displayed in the GUI.
   - The app tracks which window is currently active and annotates log entries accordingly.
   - Clipboard captures (Ctrl+C) are also logged for security analysis.

3. **Periodic Actions:**  
   - Logs are automatically saved at set intervals.
   - Every 30 seconds, if any new logs are present, they are emailed to the configured address using SMTP and the `email` module.

4. **Remote Commands:**  
   - The keylogger can be remotely started or stopped by receiving specific email commands (using `imaplib`).

5. **Process Detection:**  
   - The PyQt5-based detector scans running processes using `psutil` and can detect if the keylogger is active, offering a kill-switch for security.

6. **File Management:**  
   - Logs are auto-saved to disk for persistence.
   - You can manually save logs via the GUI, and review key frequency statistics.

**Why I Built This Project:**

- **Learning Purpose:**  
  I wanted to deeply explore the technical workings of keyloggers, not for malicious use, but to understand how such threats operate so I can build better defenses.
- **Security Awareness:**  
  By creating both the keylogger and a detector, I aimed to learn how to prevent and detect keylogging in real-world systems.
- **Python Automation:**  
  Practicing Python event handling, GUI development, concurrency, and email automation.
- **Ethical Hacking & Education:**  
  The project is a hands-on resource for anyone learning cybersecurity, ethical hacking, or Python scripting.

---

## ⚙️ Tech Stack

- **Language:** Python
- **GUI Frameworks:** 
  - `tkinter` (main app)
  - `ttkbootstrap` (themed GUI)
  - `PyQt5` (detector utility)
- **Keylogging:** `pynput`
- **Process Scanning:** `psutil`
- **Clipboard Access:** `pyperclip`
- **Window Info:** `win32gui`
- **Email Transmission:** 
  - `smtplib`
  - `email.message`, `email` (parsing & composing)
  - `imaplib` (receive commands)
- **File Handling:** `os`, `filedialog`, `messagebox`
- **Concurrency:** `threading`
- **Utilities:** `collections.defaultdict`, `time`, `sys`
- **Other:** All modules are open source and installable via pip.
- **License:** GNU GPL v3.0

---

## 📁 File Structure

```
Email-Based-Keylogger/
├── tk_keylogger.py         # Main keylogger logic (Tkinter/ttkbootstrap)
├── keylogger_detector.py   # PyQt5 GUI for process/keylogger detection
├── requirements.txt        # Python dependencies
├── LICENSE                 # GPL v3.0 License
├── README.md               # This documentation
```

---

## ⚡ How to Run Locally

### 1. Clone the Repository

```bash
git clone https://github.com/Sattwik999/Email-Based-Keylogger.git
cd Email-Based-Keylogger
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Your Email

- Open `tk_keylogger.py` and set your email credentials (`EMAIL_SENDER`, `EMAIL_PASSWORD`, `EMAIL_RECEIVER`).
- For Gmail, you may need to enable "App Passwords" or "Allow less secure apps".

### 4. Run the Keylogger

```bash
python tk_keylogger.py
```

### 5. Run the Detector (Optional)

```bash
python keylogger_detector.py
```

### 6. Stop Logging

- Use `Ctrl+C` in the terminal or close the process.

---

## 🌟 Features

- Background keylogging with `pynput`
- Logs sent securely via email
- Customizable reporting interval
- Simple, extensible Python codebase
- Clipboard capture
- Process scanner for keylogger detection (PyQt5 GUI)
- Save logs to files
- Auto-save and auto-email logs
- Remote start/stop via email commands

---
## 🛠️ Future Plans

- Add support for encrypted log files
- Cross-platform compatibility improvements
- GUI-based configuration
- Error handling and logging enhancements

---

## 🤝 Contributing

Contributions are welcome! To get started:

1. Fork the repo & create your feature branch:
   ```bash
   git checkout -b feature/your-feature
   ```
2. Commit your changes:
   ```bash
   git commit -am "Add new feature"
   ```
3. Push to your branch:
   ```bash
   git push origin feature/your-feature
   ```
4. Open a Pull Request on GitHub.

---

## 👤 Author

**Sattwik Sarkar**

- [LinkedIn](https://www.linkedin.com/in/sattwik-sarkar999)
- [Portfolio](http://www.sattwiksarkar.me/)
- [More Projects](https://github.com/Sattwik999)

---

## 📄 License

This project is licensed under the GNU GPL v3.0. See the `LICENSE` file for details.

---

## 💬 Questions & Support

For questions or issues, open an issue on GitHub or contact me directly!

---

**⭐ Star this repository if you found it helpful!**

*Learning cybersecurity and automation, one script at a time.*
