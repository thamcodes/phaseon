# Import Libraries
import sys
import numpy as np
import pyqtgraph as pg
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                             QFrame, QGraphicsDropShadowEffect, QGridLayout)
from PyQt6.QtCore import Qt, QTimer, QRectF
from PyQt6.QtGui import QFont, QColor, QPainter, QPen
from datetime import datetime

# Color Scheme
bg_color = "#F3F4F6"         # Anti-Flash White
white_color = "#FFFFFF"      # White
primary_color = "#059669"    # Emerald Green 
attention_color = "#047857"  # Dark Green 
relax_color = "#34D399"      # Cool Green
beta_color = "#EF4444"       # Coral Red
alpha_color = "#10B981"      # Strong Cyan
text_dark_color = "#1F2937"  # Midnight
text_light_color = "#9CA3AF" # Ashy Blue
accent_red_color = "#EF4444" # Coral Red

# Calibration Class
class CalibrationScreen(QWidget):
    def __init__(self, mode_name, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Calibration In Progress")
        
        # Window Settings
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        self.setStyleSheet("background-color: black;")
        self.showFullScreen()

        # Window Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)
        layout.addStretch()

        # Main Text
        self.lbl_status = QLabel(f"Calibrating {mode_name}...")
        self.lbl_status.setStyleSheet(f"color: {relax_color}; font-size: 48px; font-weight: bold; font-family: 'Roboto';")
        self.lbl_status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.lbl_status)

        # Subtext
        lbl_sub = QLabel("Please remain still and relax.")
        lbl_sub.setStyleSheet("color: #888; font-size: 24px;")
        lbl_sub.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(lbl_sub)

        layout.addStretch()

        # Cancel Button
        self.btn_cancel = QPushButton("Cancel / Exit")
        self.btn_cancel.setCursor(Qt.CursorShape.PointingHandCursor)
        self.btn_cancel.setFixedSize(200, 60)
        self.btn_cancel.setStyleSheet(f"""
            QPushButton {{
                background-color: {accent_red_color}; color: white; 
                border-radius: 10px; font-size: 18px; font-weight: bold;
            }}
            QPushButton:hover {{ background-color: #C53030; }}
        """)
        self.btn_cancel.clicked.connect(self.close)
        
        # Center the button horizontally
        btn_container = QHBoxLayout()
        btn_container.addStretch()
        btn_container.addWidget(self.btn_cancel)
        btn_container.addStretch()
        layout.addLayout(btn_container)

        layout.addSpacing(50)

        # Duration
        self.timer = QTimer()
        self.timer.setSingleShot(True)
        self.timer.timeout.connect(self.finish_calibration)
        self.timer.start(30000) 

    def finish_calibration(self):
        self.close()


# Attention/Relaxation Odometer Class
class MentalOdometer(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedSize(340, 180)
        self.setStyleSheet(f"background-color: {white_color}; border-radius: 16px;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15); shadow.setColor(QColor(0, 0, 0, 15)); shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        self.attention = 0
        self.relaxation = 0

    # Update Values Constructor
    def update_values(self, att):
        self.attention = int(max(0, min(100, att))) 
        self.relaxation = 100 - self.attention
        self.update() 

    # Design settings for Arc
    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        width = self.width()
        x, y = 40, 25 
        rect_size = width - 80 
        rect = QRectF(x, y, rect_size, rect_size)
        arc_width = 25

        # Background Arc
        pen_bg = QPen(QColor("#E5E7EB"), arc_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.FlatCap)
        painter.setPen(pen_bg); painter.drawArc(rect, 180 * 16, -180 * 16)

        # Attention
        pen_att = QPen(QColor(attention_color), arc_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.FlatCap)
        painter.setPen(pen_att)
        att_span_degrees = (self.attention / 100.0) * 180
        painter.drawArc(rect, 180 * 16, int(-att_span_degrees * 16))

        # Relaxation
        pen_rel = QPen(QColor(relax_color), arc_width, Qt.PenStyle.SolidLine, Qt.PenCapStyle.FlatCap)
        painter.setPen(pen_rel)
        start_angle = 180 - att_span_degrees
        rel_span_degrees = (self.relaxation / 100.0) * 180
        painter.drawArc(rect, int(start_angle * 16), int(-rel_span_degrees * 16))

        # Percentages
        painter.setFont(QFont('Roboto', 28, QFont.Weight.Bold))
        painter.setPen(QColor(attention_color))
        painter.drawText(QRectF(x, y + 60, rect_size/2, 50), Qt.AlignmentFlag.AlignCenter, f"{self.attention}%")
        painter.setPen(QColor(relax_color))
        painter.drawText(QRectF(x + rect_size/2, y + 60, rect_size/2, 50), Qt.AlignmentFlag.AlignCenter, f"{self.relaxation}%")
        
        # Text
        painter.setFont(QFont('Roboto', 9, QFont.Weight.Bold))
        painter.setPen(QPen(QColor(attention_color), 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawPoint(int(x + rect_size/4 - 35), int(y + 120))
        painter.setPen(QColor(text_dark_color))
        painter.drawText(QRectF(x, y + 110, rect_size/2, 20), Qt.AlignmentFlag.AlignCenter, "Attention")
        painter.setPen(QPen(QColor(relax_color), 6, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        painter.drawPoint(int(x + (rect_size*0.75) - 38), int(y + 120))
        painter.setPen(QColor(text_dark_color))
        painter.drawText(QRectF(x + rect_size/2, y + 110, rect_size/2, 20), Qt.AlignmentFlag.AlignCenter, "Relaxation")

# Stat Card Class
class StatCard(QFrame):
    def __init__(self, title, value, subtext, is_primary=False):
        super().__init__()
        self.setFixedSize(220, 180) 

        # Card Settings
        if is_primary:
            bg, text_main, text_sub = primary_color, white_color, "#D1FAE5"
        else:
            bg, text_main, text_sub = white_color, text_dark_color, text_light_color
        self.setStyleSheet(f"background-color: {bg}; border-radius: 15px;")

        if not is_primary:
            shadow = QGraphicsDropShadowEffect()
            shadow.setBlurRadius(15); shadow.setColor(QColor(0, 0, 0, 15)); shadow.setOffset(0, 4)
            self.setGraphicsEffect(shadow)

        # Card Layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        lbl_title = QLabel(title); lbl_title.setStyleSheet(f"color: {text_sub}; font-size: 13px; font-weight: 600;")
        layout.addWidget(lbl_title)
        self.lbl_value = QLabel(value); self.lbl_value.setStyleSheet(f"color: {text_main}; font-size: 32px; font-weight: bold;")
        layout.addWidget(self.lbl_value)
        self.lbl_sub = QLabel(subtext); self.lbl_sub.setStyleSheet(f"color: {text_sub}; font-size: 11px;")
        layout.addWidget(self.lbl_sub)

    # Update Data Constructor
    def update_data(self, new_val, new_sub):
        self.lbl_value.setText(str(new_val))
        self.lbl_sub.setText(str(new_sub))

# Main Class
class PhaseonDashboard(QMainWindow):
    def __init__(self):
        super().__init__()

        # Window Settings
        self.setWindowTitle("Phaseon - Interface")
        self.resize(1280, 850)
        self.setStyleSheet(f"background-color: {bg_color}; font-family: 'Roboto'; ")

        # Data Buffer
        self.data_len = 300
        self.channels = ['O1', 'O2', 'T3', 'T4']
        self.raw_buffer = np.zeros((4, self.data_len)) 
        self.alpha_buffer = np.zeros(self.data_len)     
        self.beta_buffer = np.zeros(self.data_len)     
        self.recording_start = None

        # Main Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QHBoxLayout(central_widget)
        self.main_layout.setContentsMargins(15, 15, 15, 15)
        self.main_layout.setSpacing(0)

        # UI Elements
        self.init_sidebar()
        self.init_content_area()

        # Clock and Timer
        self.clock_timer = QTimer()
        self.clock_timer.timeout.connect(self.update_clock)
        self.clock_timer.start(1000) 

    # Sidebar Constructor
    def init_sidebar(self):
        sidebar = QFrame()
        sidebar.setFixedWidth(240)
        sidebar.setStyleSheet(f"""
            QFrame{{ background-color: {white_color}; border-right: 1px solid #E5E7EB; border-radius: 15px; }}
            QLabel{{ color: {text_light_color}; font-weight: bold; padding-left: 10px; margin-top: 10px; }}
            QPushButton{{
                text-align: left; padding: 12px 20px; border: none; border-radius: 10px;
                color: {text_dark_color}; font-weight: 600; font-size: 14px;
            }}
            QPushButton:hover{{ background-color: #EBF4DD; }}
            QPushButton:checked{{ background-color: {primary_color}; color: white; }}
        """)
        
        # Sidebar Layout
        layout = QVBoxLayout(sidebar)
        layout.setContentsMargins(20, 30, 20, 20)
        layout.setSpacing(20)

        # Menu
        brand = QLabel("Dashboard")
        brand.setStyleSheet(f"color: {primary_color}; font-size: 24px; font-weight: 800; padding-left: 5px; margin-bottom: 20px; border: none; ")
        layout.addWidget(brand)

        # Connect/Disconnect Device Button
        self.btn_connect = QPushButton("Connect Device")
        self.btn_connect.setCheckable(True)
        self.btn_connect.clicked.connect(self.toggle_connection)
        layout.addWidget(self.btn_connect)

        # Connect/Disconnect Arduino Button
        self.btn_arduino = QPushButton("Connect Arduino")
        self.btn_arduino.setCheckable(True)
        self.btn_arduino.clicked.connect(self.toggle_connection)
        layout.addWidget(self.btn_arduino)

        # IAPF Calibratin Button
        self.btn_iapf = QPushButton("IAPF Calibration")
        self.btn_iapf.setCheckable(True)
        self.btn_iapf.clicked.connect(lambda: self.start_calibration("IAPF"))
        layout.addWidget(self.btn_iapf)

        # Baseline Calibration
        self.btn_baseline = QPushButton("Baseline Calibration")
        self.btn_baseline.setCheckable(True)
        self.btn_baseline.clicked.connect(lambda: self.start_calibration("Baseline"))
        layout.addWidget(self.btn_baseline)

        # Resistances
        layout.addSpacing(20)
        quality_label = QLabel("Resistance")
        quality_label.setStyleSheet(f"color: {text_dark_color}; font-size: 14px")
        layout.addWidget(quality_label)

            # Container for the 4 channel indicators
        quality_container = QFrame()
        quality_container.setStyleSheet("border: none; border-radius: 10px; padding: 5px;")
        q_layout = QGridLayout(quality_container)
       
        self.quality_leds = {}
        channels = [('O1', 0, 0), ('O2', 0, 1), ('T3', 1, 0), ('T4', 1, 1)]
       
            # Matrix and Style
        for ch, row, col in channels:
            v_box = QVBoxLayout()
            led = QLabel()
            led.setFixedSize(14, 14)
            led.setStyleSheet("background-color: #D1D5DB; border-radius: 7px; border: 1px solid #9CA3AF;")
            lbl = QLabel(ch)
            lbl.setStyleSheet("font-size: 10px; color: {text_light_color}; font-weight: normal; margin-top: 0px;")
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            v_box.addWidget(led, alignment=Qt.AlignmentFlag.AlignCenter)
            v_box.addWidget(lbl, alignment=Qt.AlignmentFlag.AlignCenter)
            q_layout.addLayout(v_box, row, col)
            self.quality_leds[ch] = led
        layout.addWidget(quality_container)
        self.lbl_resistance = QLabel()
        
        layout.addStretch()
        self.main_layout.addWidget(sidebar) 

    # Content Area Constructor
    def init_content_area(self):
        content_area = QWidget()
        layout = QVBoxLayout(content_area)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(30)

        # Content Area Layout
        header_layout = QHBoxLayout()
        title = QLabel("Phaseon")
        title.setStyleSheet(f"color: {text_dark_color}; font-size: 28px; font-weight: bold;")
        header_layout.addWidget(title)
        
        header_layout.addStretch() 
        
        # Device Badge
        self.device_badge = QLabel(" ● Device Disconnected ")
        self.device_badge.setStyleSheet(f"background-color: #FEE2E2; color: {accent_red_color}; border-radius: 15px; padding: 5px 15px; font-weight: bold;")
        header_layout.addWidget(self.device_badge)
        header_layout.addSpacing(10) 

        # Arduino Badge
        self.arduino_badge = QLabel(" ● Arduino Disconnected ")
        self.arduino_badge.setStyleSheet(f"background-color: #FEE2E2; color: {accent_red_color}; border-radius: 15px; padding: 5px 15px; font-weight: bold;")
        header_layout.addWidget(self.arduino_badge)
        
        layout.addLayout(header_layout)

        # Card Layout
        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(25)

        # Odometer Card
        self.odometer = MentalOdometer()
        self.card_state = StatCard("Dominant State", "-", "Waiting for data...", is_primary=True)

        # Record Card
        self.record_card = QFrame()
        self.record_card.setFixedSize(220, 180)
        self.record_card.setStyleSheet(f"background-color: {text_dark_color}; border-radius: 15px;")
        
            # Layout for Record
        rec_layout = QVBoxLayout(self.record_card)
        rec_title = QLabel("Session Duration")
        rec_title.setStyleSheet("color: #9CA3AF; font-size: 12px;")
        self.lbl_timer = QLabel("00:00:00")
        self.lbl_timer.setStyleSheet("color: white; font-size: 32px; font-weight: bold;")
            
            # Clock and Time
        time_info_layout = QHBoxLayout()
        self.lbl_start = QLabel("Start: --:--")
        self.lbl_end = QLabel("End: --:--")
        self.lbl_start.setStyleSheet("color: #9CA3AF; font-size: 12px;")
        self.lbl_end.setStyleSheet("color: #9CA3AF; font-size: 12px;")
        time_info_layout.addWidget(self.lbl_start)
        time_info_layout.addStretch()
        time_info_layout.addWidget(self.lbl_end)

            # Record Button
        self.btn_record = QPushButton("Start Recording")
        self.btn_record.setStyleSheet(f"background-color: {primary_color}; color: white; border-radius: 8px; padding: 8px; font-weight: bold; margin-top: 5px;")
        self.btn_record.setCheckable(True)
        self.btn_record.clicked.connect(self.toggle_record)

        rec_layout.addWidget(rec_title)
        rec_layout.addWidget(self.lbl_timer)
        rec_layout.addLayout(time_info_layout)
        rec_layout.addStretch()
        rec_layout.addWidget(self.btn_record)

        stats_layout.addWidget(self.odometer)
        stats_layout.addWidget(self.card_state)
        stats_layout.addWidget(self.record_card)
        stats_layout.addStretch()
        layout.addLayout(stats_layout)

        # Graphs
            # Alpha/Beta Waves
        wave_container = QFrame()
        wave_container.setFixedHeight(200)
        wave_container.setStyleSheet(f"background-color: {white_color}; border-radius: 20px;")
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20); shadow.setColor(QColor(0, 0, 0, 10)); shadow.setOffset(0, 5)
        wave_container.setGraphicsEffect(shadow)
        wave_layout = QVBoxLayout(wave_container)
        wave_layout.setContentsMargins(20, 10, 20, 10)
            
        wave_header = QHBoxLayout()
        wave_header.addWidget(QLabel("Alpha & Beta Waves"))
        lbl_legend = QLabel("■ Alpha (Relax)   ■ Beta (Focus)")
        lbl_legend.setStyleSheet(f"color: {text_light_color}; font-size: 11px; font-weight: bold;")
        wave_header.addWidget(lbl_legend)
        wave_layout.addLayout(wave_header)

            # Styles for Alpha/Beta Graph
        self.wave_widget = pg.GraphicsLayoutWidget()
        self.wave_widget.setBackground('w')
        p_wave = self.wave_widget.addPlot()
        p_wave.showGrid(x=False, y=True, alpha=0.1)
        p_wave.getAxis('left').setPen('#DDD')
        p_wave.hideAxis('bottom')
        p_wave.setMouseEnabled(x=False, y=False)
        p_wave.setYRange(0, 100)

        self.curve_alpha = p_wave.plot(pen=pg.mkPen(color=alpha_color, width=2))
        self.curve_beta = p_wave.plot(pen=pg.mkPen(color=beta_color, width=2))
        wave_layout.addWidget(self.wave_widget)
        layout.addWidget(wave_container)

            # Raw EEG Graph
        chart_container = QFrame()
        chart_container.setStyleSheet(f"background-color: {white_color}; border-radius: 20px;")
        shadow2 = QGraphicsDropShadowEffect()
        shadow2.setBlurRadius(20); shadow2.setColor(QColor(0, 0, 0, 10)); shadow2.setOffset(0, 5)
        chart_container.setGraphicsEffect(shadow2)
        chart_layout = QVBoxLayout(chart_container)
        chart_layout.setContentsMargins(20, 10, 20, 10)
        chart_layout.addWidget(QLabel("Live Raw EEG"))

            # Styles for Raw Graph
        self.graph_widget = pg.GraphicsLayoutWidget()
        self.graph_widget.setBackground('w') 
        self.plots = []
        self.curves = []
        line_colors = ["#1F2937", "#059669", "#7C3AED", "#D97706"] 
        axis_color = "#DDD"
        label_style = {'color': axis_color, 'font-size': '10pt', 'font-weight': 'bold'}

        for i, ch_name in enumerate(self.channels):
            p = self.graph_widget.addPlot(row=i, col=0)
            p.showGrid(x=False, y=True, alpha=0.1)
            p.hideButtons()
            p.setMenuEnabled(False)
            p.setMouseEnabled(x=False, y=False)
            p.setLabel('left', ch_name, **label_style)
            ax = p.getAxis('left')
            ax.setPen(pg.mkPen(color=axis_color, width=1))
            ax.setTextPen(pg.mkPen(color=axis_color))
            p.hideAxis('bottom')
            p.setYRange(-50, 50)
            curve = p.plot(pen=pg.mkPen(color=line_colors[i], width=1.5))
            self.plots.append(p)
            self.curves.append(curve)

        chart_layout.addWidget(self.graph_widget)
        layout.addWidget(chart_container, stretch=1)
        self.main_layout.addWidget(content_area)

    # Calibration Constructor
    def start_calibration(self, mode):
        self.calib_screen = CalibrationScreen(mode)
        self.calib_screen.show()
        self.btn_iapf.setChecked(False)
        self.btn_baseline.setChecked(False)

    # Toggle Connection Constructor
    def toggle_connection(self):
        if self.btn_connect.isChecked():
            self.btn_connect.setText("Disconnect")
            self.device_badge.setText(" ● Connecting... ")
            self.device_badge.setStyleSheet(f"background-color: #FEF3C7; color: #D97706; border-radius: 15px; padding: 5px 15px; font-weight: bold;")
        else:
            self.btn_connect.setText("Connect Device")
            self.device_badge.setText(" ● Device Disconnected ")
            self.device_badge.setStyleSheet(f"background-color: #FEE2E2; color: {accent_red_color}; border-radius: 15px; padding: 5px 15px; font-weight: bold;")
        
        if self.btn_arduino.isChecked():
            self.btn_arduino.setText("Disconnect")
            self.arduino_badge.setText(" ● Connecting... ")
            self.arduino_badge.setStyleSheet(f"background-color: #FEF3C7; color: #D97706; border-radius: 15px; padding: 5px 15px; font-weight: bold;")
        else:
            self.btn_arduino.setText("Connect Arduino")
            self.arduino_badge.setText(" ● Arduino Disconnected ")
            self.arduino_badge.setStyleSheet(f"background-color: #FEE2E2; color: {accent_red_color}; border-radius: 15px; padding: 5px 15px; font-weight: bold;")
       
    # Toggle Record Constructor
    def toggle_record(self):
        if self.btn_record.isChecked():
            self.btn_record.setText("Stop")
            self.btn_record.setStyleSheet(f"background-color: {accent_red_color}; color: white; border-radius: 8px; padding: 8px; font-weight: bold; margin-top: 5px;")
            self.recording_start = datetime.now()
            self.lbl_start.setText(f"Start: {self.recording_start.strftime('%H:%M:%S')}")
            self.lbl_end.setText("End: --:--")
        else:
            self.btn_record.setText("Start Recording")
            self.btn_record.setStyleSheet(f"background-color: {primary_color}; color: white; border-radius: 8px; padding: 8px; font-weight: bold; margin-top: 5px;")
            if self.recording_start:
                end_time = datetime.now()
                self.lbl_end.setText(f"End: {end_time.strftime('%H:%M:%S')}")
                self.recording_start = None

    # Update Clock Constructor
    def update_clock(self):
        if self.recording_start:
            elapsed = datetime.now() - self.recording_start
            seconds = int(elapsed.total_seconds())
            h, m, s = seconds // 3600, (seconds % 3600) // 60, seconds % 60
            self.lbl_timer.setText(f"{h:02}:{m:02}:{s:02}")

# End Point
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhaseonDashboard()
    window.show()
    sys.exit(app.exec())