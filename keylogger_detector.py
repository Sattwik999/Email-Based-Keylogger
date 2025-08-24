import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QProgressBar, QTreeWidget,
    QTreeWidgetItem, QPushButton, QHBoxLayout, QStyleFactory, QFrame
)
from PyQt5.QtCore import Qt, QTimer
import psutil
import os

keylogger_name = "tk_keylogger.py"  # Keylogger process name
detector_name = "keylogger_detector.py"  # This script's filename (to exclude itself)

class KeyloggerDetector(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Security Scanner")
        self.setGeometry(100, 100, 700, 450)
        self.setStyleSheet("background-color: #f5f5f5; border-radius: 10px;")

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Title Label
        self.title_label = QLabel("Security Scanner")
        self.title_label.setStyleSheet("font-size: 18pt; font-weight: bold; color: #0078D4;")
        self.layout.addWidget(self.title_label, alignment=Qt.AlignCenter)

        # Status Label
        self.status_label = QLabel("🔍 Status: Idle")
        self.status_label.setStyleSheet("font-size: 12pt; color: green; padding: 5px;")
        self.status_label.setFrameStyle(QFrame.Panel | QFrame.Raised)
        self.status_label.setStyleSheet("background-color: #e1e1e1; padding: 10px; border-radius: 8px;")
        self.layout.addWidget(self.status_label, alignment=Qt.AlignCenter)

        # Scan Progress Bar
        self.progress = QProgressBar()
        self.progress.setRange(0, 0)  # Indeterminate progress bar
        self.progress.setStyleSheet("QProgressBar { border: 1px solid gray; border-radius: 5px; height: 10px; }")
        self.layout.addWidget(self.progress)
        self.progress.hide()

        # Process Table
        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Process ID", "Process Name"])
        self.tree.setColumnWidth(0, 100)
        self.tree.setColumnWidth(1, 450)
        self.tree.setStyleSheet("border-radius: 8px; background-color: white;")
        self.layout.addWidget(self.tree)

        # Button Frame
        self.btn_frame = QHBoxLayout()
        self.layout.addLayout(self.btn_frame)

        self.start_button = self.create_button("▶ Start Scan", "#0078D4", self.start_scan)
        self.stop_button = self.create_button("⏹ End Scan", "#D83B01", self.stop_scan, False)
        self.kill_button = self.create_button("🛑 Kill Process", "#D13438", self.kill_process, False)

        self.scanning = False
        self.detected_pid = None

    def create_button(self, text, color, command, enabled=True):
        button = QPushButton(text)
        button.setStyleSheet(f"background-color: {color}; color: white; padding: 8px; border-radius: 5px;")
        button.clicked.connect(command)
        button.setEnabled(enabled)
        self.btn_frame.addWidget(button)
        return button

    def start_scan(self):
        self.scanning = True
        self.status_label.setText("🔍 Status: Scanning...")
        self.status_label.setStyleSheet("background-color: #ffcc00; padding: 10px; border-radius: 8px;")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.progress.show()
        self.timer = QTimer()
        self.timer.timeout.connect(self.scan_processes)
        self.timer.start(5000)  # Scan every 5 seconds

    def stop_scan(self):
        self.scanning = False
        self.status_label.setText("🛑 Status: Scan Stopped")
        self.status_label.setStyleSheet("background-color: #D83B01; color: white; padding: 10px; border-radius: 8px;")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.progress.hide()
        self.timer.stop()

    def scan_processes(self):
        existing_pids = set()
        for i in range(self.tree.topLevelItemCount()):
            item = self.tree.topLevelItem(i)
            existing_pids.add(int(item.text(0)))

        detected_pids = []
        current_pid = os.getpid()
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                process_name = proc.info['name']
                process_cmd = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                if proc.info['pid'] == current_pid:
                    continue
                if keylogger_name in process_cmd or keylogger_name == process_name:
                    if proc.info['pid'] not in existing_pids:
                        item = QTreeWidgetItem([str(proc.info['pid']), process_name])
                        item.setForeground(0, Qt.red)
                        item.setForeground(1, Qt.red)
                        self.tree.addTopLevelItem(item)
                    detected_pids.append(proc.info['pid'])
                    self.detected_pid = proc.info['pid']
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

        for i in reversed(range(self.tree.topLevelItemCount())):
            item = self.tree.topLevelItem(i)
            pid = int(item.text(0))
            if pid not in detected_pids:
                self.tree.takeTopLevelItem(i)

        if detected_pids:
            self.status_label.setText("⚠️ Keylogger Detected!")
            self.status_label.setStyleSheet("background-color: #D13438; color: white; padding: 10px; border-radius: 8px;")
            self.kill_button.setEnabled(True)
        else:
            self.status_label.setText("✅ No Keylogger Found")
            self.status_label.setStyleSheet("background-color: #107C10; color: white; padding: 10px; border-radius: 8px;")
            self.kill_button.setEnabled(False)

    def kill_process(self):
        if self.detected_pid:
            try:
                psutil.Process(self.detected_pid).terminate()
                self.status_label.setText(f"🛑 Keylogger (PID {self.detected_pid}) Terminated Successfully!")
                self.status_label.setStyleSheet("background-color: #0078D4; color: white; padding: 10px; border-radius: 8px;")
                self.kill_button.setEnabled(False)
                self.tree.clear()
            except Exception as e:
                self.status_label.setText(f"⚠️ Error: {e}")
                self.status_label.setStyleSheet("background-color: #D13438; color: white; padding: 10px; border-radius: 8px;")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    window = KeyloggerDetector()
    window.show()
    sys.exit(app.exec_())
