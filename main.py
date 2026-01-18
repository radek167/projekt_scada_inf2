import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QSlider, QFrame, QCheckBox, QProgressBar, QComboBox, QButtonGroup
from PyQt5.QtCore import QTimer, Qt, QRectF, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPolygonF, QFont, QPainterPath

class Scada:
    def __init__(self, x, y, w, h, name):
        self.x = float(x)
        self.y = float(y)
        self.width = float(w)
        self.height = float(h)
        self.name = name

    def update(self, dt):
        pass

    def draw_content(self, painter):
        pass

    def draw(self, painter):
        painter.save()
        painter.translate(self.x, self.y)
        self.draw_content(painter)
        painter.restore()

class Rura:
    def __init__(self, x1, y1, x2, y2, color, thickness, label=""):
        self.x1 = int(x1)
        self.y1 = int(y1)
        self.x2 = int(x2)
        self.y2 = int(y2)
        self.color = color
        self.thickness = thickness
        self.label = label

    def draw(self, painter):
        painter.setPen(QPen(self.color, self.thickness, Qt.SolidLine, Qt.RoundCap))
        painter.setBrush(Qt.NoBrush)
        painter.drawLine(self.x1, self.y1, self.x2, self.y2)

        if self.label:
            mid_x = (self.x1 + self.x2) // 2
            mid_y = (self.y1 + self.y2) // 2
            painter.setFont(QFont("Arial", 8, QFont.Bold))
            fm = painter.fontMetrics()
            tw = fm.width(self.label)

            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(0, 0, 0))
            painter.drawRect(mid_x, mid_y - 12, tw + 4, 14)
            painter.setPen(self.color)
            painter.drawText(mid_x + 2, mid_y, self.label)

class ZbiornikWoda(Scada):
    def __init__(self, x, y, name):
        Scada.__init__(self, x, y, 90, 120, name)
        self.level = 80.0
        self.flow_in = 0.0
        self.flow_out = 0.0
        self.ui_label_m3 = None

    def draw_content(self, painter):
        painter.setPen(QPen(Qt.white, 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(0, 0, int(self.width), int(self.height))

        fill_h = (self.level / 100.0) * self.height
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 120, 255))
        painter.drawRect(QRectF(2, self.height - fill_h, self.width - 4, fill_h))

        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 9))
        lines = self.name.split('\n')
        for i, line in enumerate(lines):
            painter.drawText(5, 20 + (i * 15), line)

class ZbiornikWegiel(Scada):
    def __init__(self, x, y, name):
        Scada.__init__(self, x, y, 100, 150, name)
        self.amount = 0.0

    def update(self, dt):
        pass

    def draw_content(self, painter):
        p1 = QPointF(0, 0)
        p2 = QPointF(self.width, 0)
        p3 = QPointF(self.width / 2, self.height)
        path = QPolygonF([p1, p2, p3])

        painter.setPen(QPen(Qt.white, 2))
        painter.setBrush(QColor(80, 80, 80))
        painter.drawPolygon(path)

        fill_ratio = self.amount / 100.0
        fill_h = fill_ratio * self.height

        painter.save()

        clip_rect = QRectF(0, self.height - fill_h, self.width, fill_h)
        painter.setClipRect(clip_rect)

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(20, 20, 20))
        painter.drawPolygon(path)

        painter.restore()

        painter.setPen(Qt.white)
        painter.drawText(25, 30, "WĘGIEL")

        if self.amount > 20:
            painter.setPen(Qt.green)
        else:
            painter.setPen(Qt.red)

        painter.setFont(QFont("Arial", 10, QFont.Bold))
        painter.drawText(35, 50, f"{int(self.amount)}%")


class Boiler(Scada):
    def __init__(self, x, y, name):
        Scada.__init__(self, x, y, 140, 180, name)
        self.temp = 20.0
        self.pressure = 0.0
        self.steam_flow = 0.0
        self.water_level = 50.0

    def draw_content(self, painter):
        painter.setPen(QPen(Qt.white, 2))
        painter.setBrush(QColor(50, 50, 50))
        painter.drawRect(0, 0, int(self.width), int(self.height))

        fx, fy = 30, 120
        fw, fh = 80, 40
        painter.setBrush(Qt.black)
        painter.setPen(Qt.NoPen)
        painter.drawRect(fx, fy, fw, fh)

        flame_x, flame_y = fx + 20, fy - 5
        flame_w, flame_h = 40, 45
        painter.setRenderHint(QPainter.Antialiasing, True)

        path_o = QPainterPath()
        path_o.moveTo(flame_x + flame_w * 0.5, flame_y + flame_h)
        path_o.cubicTo(flame_x - flame_w * 0.2, flame_y + flame_h * 0.6,
                       flame_x + flame_w * 0.1, flame_y + flame_h * 0.1,
                       flame_x + flame_w * 0.5, flame_y)
        path_o.cubicTo(flame_x + flame_w * 0.9, flame_y + flame_h * 0.1,
                       flame_x + flame_w * 1.2, flame_y + flame_h * 0.6,
                       flame_x + flame_w * 0.5, flame_y + flame_h)
        painter.setBrush(QColor(242, 92, 25))
        painter.drawPath(path_o)

        sub_x = flame_x + flame_w * 0.15
        sub_y = flame_y + flame_h * 0.3
        sub_w, sub_h = flame_w * 0.7, flame_h * 0.7
        path_y = QPainterPath()
        path_y.moveTo(sub_x + sub_w * 0.5, sub_y + sub_h)
        path_y.cubicTo(sub_x - sub_w * 0.1, sub_y + sub_h * 0.6,
                       sub_x + sub_w * 0.3, sub_y + sub_h * 0.1,
                       sub_x + sub_w * 0.6, sub_y)
        path_y.cubicTo(sub_x + sub_w * 1.0, sub_y + sub_h * 0.3,
                       sub_x + sub_w * 0.8, sub_y + sub_h * 0.8,
                       sub_x + sub_w * 0.5, sub_y + sub_h)
        painter.setBrush(QColor(247, 237, 50))
        painter.drawPath(path_y)

        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.drawText(40, 30, self.name)

class Turbina(Scada):
    def __init__(self, x, y, name):
        Scada.__init__(self, x, y, 160, 100, name)

        self.rpm = 0.0
        self.power_mw = 0.0

    def draw_content(self, painter):
        painter.setPen(QPen(Qt.white, 2))
        painter.setBrush(QColor(70, 130, 180))
        painter.drawRect(0, 0, int(self.width), int(self.height))

        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 14, QFont.Bold))
        painter.drawText(30, 60, self.name)


class ZbiornikWodaCiepla(Scada):
    def __init__(self, x, y, name):
        Scada.__init__(self, x, y, 100, 100, name)
        self.level = 0.0
        self.max_capacity = 1000.0

    def update(self, dt):
        pass

    def draw_content(self, painter):
        painter.setPen(QPen(QColor(255, 100, 100), 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(0, 0, int(self.width), int(self.height))

        fill_h = (self.level / 100.0) * self.height

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(200, 40, 40))
        painter.drawRect(QRectF(2, self.height - fill_h, self.width - 4, fill_h))

        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 9, QFont.Bold))
        painter.drawText(10, 20, "BUFOR")
        painter.drawText(10, 40, "CIEPŁA")

        painter.setPen(Qt.yellow)
        painter.drawText(30, 80, f"{int(self.level)}%")


class Bateria(Scada):
    def __init__(self, x, y, name):
        Scada.__init__(self, x, y, 100, 140, name)
        self.charge = 50.0

    def update(self, dt):
        pass

    def draw_content(self, painter):
        painter.setPen(QPen(Qt.white, 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(0, 0, int(self.width), int(self.height))

        margin_x = 10
        active_height = self.height - 40
        fill_h = (self.charge / 100.0) * active_height

        color = QColor(0, 255, 0)
        if self.charge < 20: color = QColor(255, 0, 0)

        painter.setPen(Qt.NoPen)
        painter.setBrush(color)
        painter.drawRect(QRectF(margin_x, self.height - 30 - fill_h, self.width - 2 * margin_x, fill_h))

        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 9, QFont.Bold))
        painter.drawText(5, -10, self.name)

        painter.setBrush(Qt.black)
        painter.setPen(Qt.white)
        painter.drawRect(20, int(self.height) - 25, 60, 20)
        painter.drawText(30, int(self.height) - 10, f"{int(self.charge)}%")


class SiecEnerg(Scada):
    def __init__(self, x, y):
        Scada.__init__(self, x, y, 140, 220, "")

    def draw_content(self, painter):
        painter.setRenderHint(QPainter.Antialiasing, True)

        pen_thick = 2
        painter.setPen(QPen(Qt.white, pen_thick))
        painter.setBrush(QColor(0, 0, 0))

        cx = self.width / 2
        box_w = 36
        hw = box_w / 2
        top_y = 20
        mid_y = 80
        bot_y = 150
        leg_y = 200

        rect_top = QRectF(cx - hw, top_y, box_w, mid_y - top_y)
        painter.drawRect(rect_top)
        painter.drawLine(int(cx - hw), int(top_y), int(cx + hw), int(mid_y))
        painter.drawLine(int(cx + hw), int(top_y), int(cx - hw), int(mid_y))

        rect_bot = QRectF(cx - hw, mid_y, box_w, bot_y - mid_y)
        painter.drawRect(rect_bot)
        painter.drawLine(int(cx - hw), int(mid_y), int(cx + hw), int(bot_y))
        painter.drawLine(int(cx + hw), int(mid_y), int(cx - hw), int(bot_y))

        painter.drawLine(int(cx - hw), int(bot_y), int(cx - hw - 20), int(leg_y))
        painter.drawLine(int(cx + hw), int(bot_y), int(cx + hw + 20), int(leg_y))

        arm_len = 45

        def draw_arm(start_x, start_y, is_left):
            direction = -1 if is_left else 1
            p1 = QPointF(start_x, start_y)
            p2 = QPointF(start_x + (direction * arm_len), start_y + 5)
            p3 = QPointF(start_x + (direction * arm_len), start_y + 25)
            p4 = QPointF(start_x, start_y + 30)
            path = QPolygonF([p1, p2, p3, p4])
            painter.drawPolygon(path)
            return p3

        pt_lu = draw_arm(cx - hw, top_y, True)
        pt_ru = draw_arm(cx + hw, top_y, False)
        pt_ld = draw_arm(cx - hw, mid_y + 5, True)
        pt_rd = draw_arm(cx + hw, mid_y + 5, False)

        painter.setPen(QPen(QColor(255, 220, 50), 2))
        painter.setBrush(Qt.NoBrush)

        path = QPainterPath()
        path.moveTo(pt_lu)
        path.cubicTo(pt_lu.x() - 30, pt_lu.y() + 20, 0, pt_lu.y() - 10, 0, pt_lu.y() - 20)
        path.moveTo(pt_ru)
        path.cubicTo(pt_ru.x() + 30, pt_ru.y() + 20, self.width, pt_ru.y() - 10, self.width, pt_ru.y() - 20)
        path.moveTo(pt_ld)
        path.cubicTo(pt_ld.x() - 30, pt_ld.y() + 20, 0, pt_ld.y() - 10, 0, pt_ld.y() - 20)
        path.moveTo(pt_rd)
        path.cubicTo(pt_rd.x() + 30, pt_rd.y() + 20, self.width, pt_rd.y() - 10, self.width, pt_rd.y() - 20)

        painter.drawPath(path)

class ScadaScene(QWidget):
    def __init__(self):
        super().__init__()
        self.Scadas = []
        self.Ruras = []

        self.w1 = ZbiornikWoda(50, 50, "WODA 1\nZIMNA")
        self.w2 = ZbiornikWoda(160, 50, "WODA 2\nZIMNA")
        self.wr = ZbiornikWoda(270, 50, "WODA\nREZERWA")
        self.silo = ZbiornikWegiel(50, 400, "WĘGIEL")
        self.boiler = Boiler(350, 400, "KOCIOŁ")
        self.Turbina = Turbina(340, 180, "TURBINA")
        self.hot_res = ZbiornikWodaCiepla(550, 450, "Gorąca")
        self.bat1 = Bateria(750, 400, "AKUMULATOR 1")
        self.bat2 = Bateria(870, 400, "AKUMULATOR 2")

        self.lines = SiecEnerg(850, 20)

        self.Scadas.extend([self.w1, self.w2, self.wr, self.silo, self.boiler, self.Turbina,
                                self.hot_res, self.bat1, self.bat2, self.lines])

        self.Ruras.append(Rura(95, 170, 95, 220, QColor(0, 150, 255), 4))
        self.Ruras.append(Rura(205, 170, 205, 220, QColor(0, 150, 255), 4))
        self.Ruras.append(Rura(315, 170, 315, 450, QColor(0, 150, 255), 4))
        self.Ruras.append(Rura(95, 220, 315, 220, QColor(0, 150, 255), 4))
        self.Ruras.append(Rura(315, 450, 350, 450, QColor(0, 150, 255), 4))
        self.Ruras.append(Rura(100, 550, 350, 550, QColor(150, 150, 150), 8, "PODAJNIK"))
        self.Ruras.append(Rura(420, 400, 420, 280, Qt.white, 4, "PARA"))
        self.Ruras.append(Rura(500, 230, 700, 230, Qt.yellow, 3))
        self.Ruras.append(Rura(700, 230, 700, 350, Qt.yellow, 3))
        self.Ruras.append(Rura(700, 350, 920, 350, Qt.yellow, 3))
        self.Ruras.append(Rura(920, 350, 920, 400, Qt.yellow, 3))
        self.Ruras.append(Rura(800, 350, 800, 400, Qt.yellow, 3))
        self.Ruras.append(Rura(700,230,920,230,Qt.yellow, 3, "SIEĆ"))
        self.Ruras.append(Rura(920, 230, 920, 180, Qt.yellow, 3))
        self.Ruras.append(Rura(490, 480, 550, 480, QColor(255, 100, 100), 4))
        self.Ruras.append(Rura(600, 450, 600, 400, QColor(255, 100, 100), 4))
        self.Ruras.append(Rura(600, 400, 670, 400, QColor(255, 100, 100), 4, "MIASTO"))

    def update_simulation(self):
        dt = 0.05
        for comp in self.Scadas:
            comp.update(dt)
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(self.rect(), Qt.black)

        for conn in self.Ruras:
            conn.draw(painter)
        for comp in self.Scadas:
            comp.draw(painter)

class MiniPodglad(QWidget):
    def __init__(self, obiekt_scada):
        super().__init__()
        self.obiekt = obiekt_scada
        self.setFixedSize(int(self.obiekt.width), int(self.obiekt.height))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.obiekt.draw_content(painter)

class MiniPodglad(QWidget):
    def __init__(self, obiekt_scada):
        super().__init__()
        self.obiekt = obiekt_scada
        self.setFixedSize(int(self.obiekt.width), int(self.obiekt.height))
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        self.obiekt.draw_content(painter)

class okno_materialy(QWidget):
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.setWindowTitle("Zarządzanie materiałami")
        self.resize(1000, 550)
        self.setStyleSheet("background-color: #222; color: white;")

        main_layout = QVBoxLayout()

        ramka_wegiel = QFrame()
        ramka_wegiel.setStyleSheet("background-color: #2a2a2a; border-radius: 5px;")
        layout_wegiel = QHBoxLayout(ramka_wegiel)

        layout_wegiel.addWidget(MiniPodglad(self.scene.silo))

        col_wegiel = QVBoxLayout()

        lbl_tytul = QLabel("MAGAZYN WĘGLA")
        lbl_tytul.setStyleSheet("font-weight: bold; color: orange; font-size: 14px;")
        col_wegiel.addWidget(lbl_tytul)

        self.lbl_wolne = QLabel("Wolne: ... %")
        self.lbl_wolne.setStyleSheet("color: #aaa;")
        col_wegiel.addWidget(self.lbl_wolne)

        self.slider_wegiel = QSlider(Qt.Horizontal)
        self.slider_wegiel.setMinimum(0)
        self.slider_wegiel.setMaximum(0)
        self.slider_wegiel.setStyleSheet("QSlider::handle:horizontal { background: orange; }")

        self.slider_wegiel.valueChanged.connect(self.aktualizuj_etykiete_suwaka_wegla)
        col_wegiel.addWidget(self.slider_wegiel)

        self.lbl_wybrano = QLabel("Wybrano: 0 %")
        self.lbl_wybrano.setStyleSheet("color: orange; font-weight: bold;")
        col_wegiel.addWidget(self.lbl_wybrano)

        self.btn_dostawa = QPushButton("ZATWIERDŹ DOSTAWĘ")
        self.btn_dostawa.setFixedHeight(40)
        self.btn_dostawa.setStyleSheet("background-color: #444; color: orange; border: 1px solid orange;")
        self.btn_dostawa.clicked.connect(self.wykonaj_dostawe)
        col_wegiel.addWidget(self.btn_dostawa)

        self.lbl_tonaz = QLabel("Stan: 0 / 800 t")
        col_wegiel.addWidget(self.lbl_tonaz)

        layout_wegiel.addLayout(col_wegiel)
        main_layout.addWidget(ramka_wegiel)

        lbl_woda = QLabel("STEROWNIA PRZEPŁYWU WODY (1000 m³)")
        lbl_woda.setStyleSheet("font-weight: bold; color: cyan; font-size: 14px; margin-top: 10px;")
        lbl_woda.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(lbl_woda)

        woda_container = QHBoxLayout()

        def stworz_panel_pionowy(zbiornik, nazwa):
            frame = QFrame()
            frame.setStyleSheet("background-color: #2a2a2a; border-radius: 5px;")

            v_layout = QVBoxLayout(frame)

            lbl_name = QLabel(nazwa)
            lbl_name.setStyleSheet("font-weight: bold; font-size: 12px; color: cyan;")
            lbl_name.setAlignment(Qt.AlignCenter)
            v_layout.addWidget(lbl_name)

            grafika = MiniPodglad(zbiornik)
            h_center = QHBoxLayout()
            h_center.addStretch()
            h_center.addWidget(grafika)
            h_center.addStretch()
            v_layout.addLayout(h_center)

            lbl_in = QLabel("Dopływ: 0%")
            lbl_in.setStyleSheet("font-size: 10px; color: #aaa;")
            v_layout.addWidget(lbl_in)

            sl_in = QSlider(Qt.Horizontal)
            sl_in.setRange(0, 100)
            sl_in.setStyleSheet("QSlider::handle:horizontal { background: cyan; height: 10px; }")
            v_layout.addWidget(sl_in)

            lbl_out = QLabel("Odpływ: 0%")
            lbl_out.setStyleSheet("font-size: 10px; color: #aaa;")
            v_layout.addWidget(lbl_out)

            sl_out = QSlider(Qt.Horizontal)
            sl_out.setRange(0, 100)
            sl_out.setStyleSheet("QSlider::handle:horizontal { background: #ff5555; height: 10px; }")
            v_layout.addWidget(sl_out)

            btn_set = QPushButton("USTAW")
            btn_set.setStyleSheet("background-color: #004488; color: white; border: none; padding: 5px;")
            v_layout.addWidget(btn_set)

            lbl_info = QLabel("0 m³")
            lbl_info.setAlignment(Qt.AlignCenter)
            lbl_info.setStyleSheet("font-size: 10px; color: white;")
            zbiornik.ui_label_m3 = lbl_info
            v_layout.addWidget(lbl_info)

            def on_in_change(val):
                lbl_in.setText(f"Dopływ: {val}%")

            def on_out_change(val):
                lbl_out.setText(f"Odpływ: {val}%")

            def on_click():
                self.zatwierdz_przeplyw(zbiornik, sl_in, sl_out)

            sl_in.valueChanged.connect(on_in_change)
            sl_out.valueChanged.connect(on_out_change)
            btn_set.clicked.connect(on_click)

            return frame

        woda_container.addWidget(stworz_panel_pionowy(self.scene.w1, "ZB. GŁÓWNY 1"))
        woda_container.addWidget(stworz_panel_pionowy(self.scene.w2, "ZB. GŁÓWNY 2"))
        woda_container.addWidget(stworz_panel_pionowy(self.scene.wr, "REZERWA"))

        main_layout.addLayout(woda_container)

        self.setLayout(main_layout)

        self.timer_logic = QTimer(self)
        self.timer_logic.timeout.connect(self.update_logic)
        self.timer_logic.start(100)

    def aktualizuj_etykiete_suwaka_wegla(self, val):
        tony_wybrane = (val / 100.0) * 800.0
        self.lbl_wybrano.setText(f"Wybrano: {val}% ({int(tony_wybrane)} t)")

    def wykonaj_dostawe(self):
        val = self.slider_wegiel.value()
        if val > 0:
            self.scene.silo.amount += val
            self.slider_wegiel.setValue(0)
            self.lbl_wybrano.setText("Wybrano: 0 %")

    def zatwierdz_przeplyw(self, zbiornik, slider_in, slider_out):
        zbiornik.flow_in = float(slider_in.value())
        zbiornik.flow_out = float(slider_out.value())

    def update_logic(self):
        obecny_poziom_proc = self.scene.silo.amount
        wolne_miejsce = 100.0 - obecny_poziom_proc
        self.lbl_wolne.setText(f"Wolne: {int(wolne_miejsce)}%")

        obecne_tony = (obecny_poziom_proc / 100.0) * 800.0
        self.lbl_tonaz.setText(f"Stan: {int(obecne_tony)} / 800 t")

        max_dostawa = int(wolne_miejsce)
        self.slider_wegiel.setMaximum(max_dostawa)
        if self.slider_wegiel.value() > max_dostawa:
            self.slider_wegiel.setValue(max_dostawa)

        POJEMNOSC_ZBIORNIKA_M3 = 1000.0
        MAX_PRZEPUSTOWOSC_RURY = 5.0

        for z in [self.scene.w1, self.scene.w2, self.scene.wr]:
            if hasattr(z, 'flow_in'):
                wplyw_m3 = (z.flow_in / 100.0) * MAX_PRZEPUSTOWOSC_RURY
                wyplyw_m3 = (z.flow_out / 100.0) * MAX_PRZEPUSTOWOSC_RURY

                bilans_m3 = wplyw_m3 - wyplyw_m3
                delta_procent = (bilans_m3 / POJEMNOSC_ZBIORNIKA_M3) * 100.0

                z.level = max(0.0, min(100.0, z.level + delta_procent))

                if hasattr(z, 'ui_label_m3') and z.ui_label_m3:
                    aktualne_m3 = (z.level / 100.0) * POJEMNOSC_ZBIORNIKA_M3
                    znak = "+" if bilans_m3 >= 0 else ""
                    str_bilans = f"{znak}{bilans_m3:.2f}"
                    z.ui_label_m3.setText(
                        f"{aktualne_m3:.1f} m³\n"
                        f"Bilans: {str_bilans}"
                    )

class okno_generacja(QWidget):
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.setWindowTitle("Generacja")
        self.resize(1000, 600)

        self.setStyleSheet("""
            QWidget { background-color: #1a1a1a; color: #eee; font-family: Arial; }
            QLabel { font-size: 12px; }
            QSlider::handle:horizontal { background: #ff9900; width: 20px; border-radius: 5px; }
            QProgressBar { border: 1px solid #555; text-align: center; color: white; font-weight: bold; }
            QProgressBar::chunk { background-color: #ff9900; }
        """)

        self.tank_val = 500.0

        layout = QHBoxLayout(self)

        col_boiler = QVBoxLayout()

        frame_boiler = QFrame()
        frame_boiler.setStyleSheet("background-color: #222; border: 1px solid #444;")
        lay_fb = QVBoxLayout(frame_boiler)
        lay_fb.addWidget(QLabel("1. KOCIOŁ PAROWY"))
        lay_fb.addWidget(MiniPodglad(self.scene.boiler))
        col_boiler.addWidget(frame_boiler)

        self.lbl_feed = QLabel("PALENISKO (WĘGIEL): 0%")
        self.lbl_feed.setStyleSheet("color: orange; font-weight: bold;")
        col_boiler.addWidget(self.lbl_feed)
        self.slider_feed = QSlider(Qt.Horizontal)
        self.slider_feed.setRange(0, 100)
        self.slider_feed.valueChanged.connect(self.update_labels)
        col_boiler.addWidget(self.slider_feed)

        self.bar_temp = QProgressBar()
        self.bar_temp.setRange(0, 300)
        self.bar_temp.setFormat("Temp: %v °C")
        self.bar_temp.setStyleSheet("QProgressBar::chunk { background-color: #d63030; }")
        col_boiler.addWidget(self.bar_temp)

        self.bar_press = QProgressBar()
        self.bar_press.setRange(0, 150)
        self.bar_press.setFormat("Ciśnienie: %v bar")
        self.bar_press.setStyleSheet("QProgressBar::chunk { background-color: #30d6d6; }")
        col_boiler.addWidget(self.bar_press)

        self.bar_boiler_water = QProgressBar()
        self.bar_boiler_water.setRange(0, 100)
        self.bar_boiler_water.setFormat("Woda w kotle: %v %")
        self.bar_boiler_water.setStyleSheet("QProgressBar::chunk { background-color: #0088ff; }")
        col_boiler.addWidget(self.bar_boiler_water)

        frame_tank = QFrame()
        frame_tank.setStyleSheet("background-color: #001122; border-radius: 5px; margin-top: 10px; padding: 5px;")
        lay_ft = QVBoxLayout(frame_tank)

        lay_ft.addWidget(QLabel("ZBIORNIK WODY ZASILAJĄCEJ"))

        self.bar_tank = QProgressBar()
        self.bar_tank.setRange(0, 1000)
        self.bar_tank.setFormat("%v m³")
        self.bar_tank.setStyleSheet("QProgressBar::chunk { background-color: #004488; }")
        lay_ft.addWidget(self.bar_tank)

        self.lbl_inflow_info = QLabel("Dopływ z rurociągów (W1+W2+WR): 0 m³/h")
        self.lbl_inflow_info.setStyleSheet("color: cyan; font-size: 11px;")
        lay_ft.addWidget(self.lbl_inflow_info)

        lay_ft.addWidget(QLabel("POMPA KOTŁOWA (Tłoczenie do kotła)"))
        self.slider_pump = QSlider(Qt.Horizontal)
        self.slider_pump.setStyleSheet("QSlider::handle:horizontal { background: #0088ff; }")
        lay_ft.addWidget(self.slider_pump)

        col_boiler.addWidget(frame_tank)
        col_boiler.addStretch()
        layout.addLayout(col_boiler)

        col_res = QVBoxLayout()
        frame_res = QFrame()
        frame_res.setStyleSheet("background-color: #222; border: 1px solid #444;")
        lay_fr = QVBoxLayout(frame_res)
        lay_fr.addWidget(QLabel("2. BUFOR CIEPŁA"))
        lay_fr.addWidget(MiniPodglad(self.scene.hot_res))
        col_res.addWidget(frame_res)

        box_dump = QFrame()
        box_dump.setStyleSheet("background-color: #331111; border-radius: 5px; padding: 5px;")
        lay_bd = QVBoxLayout(box_dump)
        self.lbl_valve_status = QLabel("Wymagane > 110°C")
        self.lbl_valve_status.setStyleSheet("color: gray;")
        lay_bd.addWidget(self.lbl_valve_status)
        self.chk_to_reserve = QCheckBox("ZRZUT DO BUFORA")
        self.chk_to_reserve.setEnabled(False)
        lay_bd.addWidget(self.chk_to_reserve)
        col_res.addWidget(box_dump)

        col_res.addWidget(QLabel("ZASILANIE MIASTA"))
        self.slider_city = QSlider(Qt.Horizontal)
        self.slider_city.setRange(0, 100)
        self.slider_city.setStyleSheet("QSlider::handle:horizontal { background: #ff4444; }")
        self.slider_city.valueChanged.connect(self.update_labels)
        col_res.addWidget(self.slider_city)
        self.lbl_city_flow = QLabel("...")
        self.lbl_city_flow.setAlignment(Qt.AlignCenter)
        col_res.addWidget(self.lbl_city_flow)
        col_res.addStretch()
        layout.addLayout(col_res)

        col_turbine = QVBoxLayout()
        frame_turb = QFrame()
        frame_turb.setStyleSheet("background-color: #222; border: 1px solid #444;")
        lay_fturb = QVBoxLayout(frame_turb)
        lay_fturb.addWidget(QLabel("3. TURBINA"))
        lay_fturb.addWidget(MiniPodglad(self.scene.Turbina))
        col_turbine.addWidget(frame_turb)

        self.lbl_rpm = QLabel("0 RPM")
        self.lbl_rpm.setStyleSheet("font-size: 20px; font-weight: bold; color: cyan;")
        self.lbl_rpm.setAlignment(Qt.AlignCenter)
        col_turbine.addWidget(self.lbl_rpm)
        self.bar_rpm = QProgressBar()
        self.bar_rpm.setRange(0, 3500)
        self.bar_rpm.setTextVisible(False)
        col_turbine.addWidget(self.bar_rpm)
        self.lbl_mw = QLabel("0.0 MW")
        self.lbl_mw.setStyleSheet("font-size: 28px; font-weight: bold; color: #00ff00; margin-top: 20px;")
        self.lbl_mw.setAlignment(Qt.AlignCenter)
        col_turbine.addWidget(self.lbl_mw)
        col_turbine.addStretch()
        layout.addLayout(col_turbine)

        self.physics_timer = QTimer(self)
        self.physics_timer.timeout.connect(self.update_physics)
        self.physics_timer.start(100)

    def update_labels(self):
        self.lbl_feed.setText(f"PALENISKO (WĘGIEL): {self.slider_feed.value()}%")

    def update_physics(self):
        dt = 0.1

        inflow_sum = 0.0

        if self.scene.w1.level > 0: inflow_sum += self.scene.w1.flow_out
        if self.scene.w2.level > 0: inflow_sum += self.scene.w2.flow_out
        if self.scene.wr.level > 0: inflow_sum += self.scene.wr.flow_out

        real_inflow = inflow_sum * 0.05

        self.tank_val += real_inflow * dt

        self.lbl_inflow_info.setText(f"Dopływ z rurociągów (W1+W2+WR): {real_inflow:.1f} m³/jedn")

        pump_speed = self.slider_pump.value() * 0.2
        actual_pump = 0.0

        if self.tank_val > 0 and self.scene.boiler.water_level < 100:
            actual_pump = pump_speed

            max_possible = self.tank_val / dt
            if actual_pump > max_possible:
                actual_pump = max_possible

            self.tank_val -= actual_pump * dt

        if self.tank_val < 0: self.tank_val = 0
        if self.tank_val > 1000: self.tank_val = 1000
        self.bar_tank.setValue(int(self.tank_val))

        self.scene.boiler.water_level += actual_pump * 0.2 * dt

        steam_loss = 0.0
        if self.scene.boiler.pressure > 0:
            steam_loss = self.scene.boiler.pressure * 0.05
        self.scene.boiler.water_level -= steam_loss * dt

        if self.scene.boiler.water_level < 0: self.scene.boiler.water_level = 0
        if self.scene.boiler.water_level > 100: self.scene.boiler.water_level = 100

        feed = self.slider_feed.value()
        heat_gain = 0
        if self.scene.silo.amount > 0:
            burn_cost = (feed / 100.0) * 0.05
            if self.scene.silo.amount >= burn_cost:
                self.scene.silo.amount -= burn_cost
                heat_gain = feed * 0.3
            else:
                self.scene.silo.amount = 0

        heat_loss = (self.scene.boiler.temp - 20.0) * 0.02

        if self.scene.boiler.water_level <= 0: pass

        transfer_cooling = 0.0
        valve_open = self.chk_to_reserve.isChecked()
        if self.scene.boiler.temp > 110.0:
            self.chk_to_reserve.setEnabled(True)
            self.lbl_valve_status.setText("GOTOWOŚĆ")
            self.lbl_valve_status.setStyleSheet("color: green")
            if valve_open:
                if self.scene.hot_res.level < 100:
                    transfer_cooling = 15.0
                    self.scene.hot_res.level += 0.2
        else:
            if valve_open: self.chk_to_reserve.setChecked(False)
            self.chk_to_reserve.setEnabled(False)
            self.lbl_valve_status.setText("Zimny kocioł")
            self.lbl_valve_status.setStyleSheet("color: gray")

        self.scene.boiler.temp += (heat_gain - heat_loss - transfer_cooling) * dt
        self.scene.boiler.temp = max(20.0, min(600.0, self.scene.boiler.temp))

        target_p = 0
        if self.scene.boiler.temp > 100 and self.scene.boiler.water_level > 0:
            target_p = (self.scene.boiler.temp - 100) * 0.5

        inertia = 0.05 if self.scene.boiler.water_level > 0 else 0.2
        self.scene.boiler.pressure += (target_p - self.scene.boiler.pressure) * inertia

        city_demand = self.slider_city.value()
        if self.scene.hot_res.level > 0:
            drain = (city_demand / 100.0) * 0.1
            self.scene.hot_res.level -= drain
        self.scene.hot_res.level = max(0.0, min(100.0, self.scene.hot_res.level))

        p_in = self.scene.boiler.pressure
        torque = 0
        if p_in > 20: torque = (p_in - 20) * 2.0
        friction = self.scene.Turbina.rpm * 0.05
        load = 0
        if self.scene.Turbina.rpm > 2500: load = (self.scene.Turbina.rpm - 2500) * 0.5

        self.scene.Turbina.rpm += (torque - friction - load) * dt
        if self.scene.Turbina.rpm < 0: self.scene.Turbina.rpm = 0

        mw = 0
        if self.scene.Turbina.rpm > 0:
            mw = (self.scene.Turbina.rpm / 3000.0) * 50.0
            if mw > 55: mw = 55
        self.scene.Turbina.power_mw = mw

        self.bar_temp.setValue(int(self.scene.boiler.temp))
        self.bar_press.setValue(int(self.scene.boiler.pressure))
        self.bar_boiler_water.setValue(int(self.scene.boiler.water_level))
        self.lbl_rpm.setText(f"{int(self.scene.Turbina.rpm)} RPM")
        self.bar_rpm.setValue(int(self.scene.Turbina.rpm))
        self.lbl_mw.setText(f"{mw:.1f} MW")

        cap = getattr(self.scene.hot_res, 'max_capacity', 1000.0)
        vol = (self.scene.hot_res.level / 100.0) * cap
        self.lbl_city_flow.setText(f"Stan: {int(vol)} m³ / {int(cap)} m³")

class okno_energia(QWidget):
    def __init__(self, scene):
        super().__init__()
        self.scene = scene
        self.setWindowTitle("ROZDZIELNIA GPZ - STEROWANIE MOCĄ")
        self.resize(1000, 600)

        self.setStyleSheet("""
            QWidget { background-color: #151515; color: #eeeeee; font-family: Arial; font-weight: bold; }

            QFrame#MainFrame { 
                background-color: #202020; 
                border: 3px solid #555; 
                border-radius: 6px; 
            }
            QFrame#SubPanel { 
                background-color: #101010; 
                border: 1px solid #333; 
                border-radius: 2px;
            }

            QLabel { border: none; font-size: 12px; background: transparent; }

            QPushButton {
                background-color: #333;
                color: #aaa;
                border: 2px outset #555;
                border-radius: 4px;
                font-size: 13px;
                min-width: 160px;
                max-width: 160px;
                min-height: 70px;
                max-height: 70px;
                margin: 5px;
            }
            QPushButton:hover { background-color: #444; border: 2px solid #777; }
            QPushButton:checked { background-color: #008800; color: white; border: 3px inset #004400; }
            QPushButton#btn_stop:checked { background-color: #aa0000; border: 3px inset #550000; }

            QCheckBox {
                spacing: 10px;
                font-size: 14px;
                color: #888;
                padding: 5px;
                border: 1px solid #444;
                background-color: #222;
            }
            QCheckBox::indicator { width: 20px; height: 20px; }

            QCheckBox::indicator:unchecked {
                background-color: #550000;
                border: 2px solid #aa0000;
            }
            QCheckBox::indicator:checked {
                background-color: #00ff00;
                border: 2px solid #fff;
            }
            QCheckBox:checked { color: white; border: 1px solid #00ff00; }
        """)

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(15)

        self.frame_top = QFrame()
        self.frame_top.setObjectName("MainFrame")
        top_layout = QHBoxLayout(self.frame_top)

        fr_gen = QFrame()
        fr_gen.setObjectName("SubPanel")
        l_gen = QVBoxLayout(fr_gen)
        l_gen.addWidget(QLabel("WEJŚCIE (TURBINA)"))
        l_gen.addWidget(MiniPodglad(self.scene.Turbina))
        self.lbl_gen = QLabel("0 MW")
        self.lbl_gen.setStyleSheet("color: yellow; font-size: 20px;")
        self.lbl_gen.setAlignment(Qt.AlignCenter)
        l_gen.addWidget(self.lbl_gen)
        top_layout.addWidget(fr_gen)

        self.arrow_1 = QLabel(">>>")
        self.arrow_1.setStyleSheet("font-size: 30px; color: gray;")
        self.arrow_1.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(self.arrow_1)

        fr_bat = QFrame()
        fr_bat.setObjectName("SubPanel")
        l_bat = QVBoxLayout(fr_bat)
        l_bat.addWidget(QLabel("BANK AKUMULATORÓW"))

        hbox_akusy = QHBoxLayout()

        v_aku1 = QVBoxLayout()
        self.chk_a = QCheckBox("SEKCJA A")
        self.chk_a.setChecked(True)
        v_aku1.addWidget(self.chk_a)
        v_aku1.addWidget(MiniPodglad(self.scene.bat1))
        hbox_akusy.addLayout(v_aku1)

        v_aku2 = QVBoxLayout()
        self.chk_b = QCheckBox("SEKCJA B")
        self.chk_b.setChecked(True)
        v_aku2.addWidget(self.chk_b)
        v_aku2.addWidget(MiniPodglad(self.scene.bat2))
        hbox_akusy.addLayout(v_aku2)

        l_bat.addLayout(hbox_akusy)

        self.lbl_bat_status = QLabel("STAN: SPOCZYNEK")
        self.lbl_bat_status.setAlignment(Qt.AlignCenter)
        self.lbl_bat_status.setStyleSheet("color: white; font-size: 14px;")
        l_bat.addWidget(self.lbl_bat_status)
        top_layout.addWidget(fr_bat)

        self.arrow_2 = QLabel(">>>")
        self.arrow_2.setStyleSheet("font-size: 30px; color: gray;")
        self.arrow_2.setAlignment(Qt.AlignCenter)
        top_layout.addWidget(self.arrow_2)

        fr_grid = QFrame()
        fr_grid.setObjectName("SubPanel")
        l_grid = QVBoxLayout(fr_grid)
        l_grid.addWidget(QLabel("WYJŚCIE (SIEĆ KSE)"))
        l_grid.addWidget(MiniPodglad(self.scene.lines))
        self.lbl_grid = QLabel("0 MW")
        self.lbl_grid.setStyleSheet("color: #00ff00; font-size: 20px;")
        self.lbl_grid.setAlignment(Qt.AlignCenter)
        l_grid.addWidget(self.lbl_grid)
        top_layout.addWidget(fr_grid)

        main_layout.addWidget(self.frame_top, stretch=2)

        self.frame_bot = QFrame()
        self.frame_bot.setObjectName("MainFrame")
        bot_layout = QHBoxLayout(self.frame_bot)

        bot_layout.addStretch()

        self.btn_group = QButtonGroup(self)

        self.btn_normal = QPushButton("PRACA NA SIEĆ\n(NORMAL)")
        self.btn_normal.setCheckable(True)
        self.btn_normal.setChecked(True)
        self.btn_group.addButton(self.btn_normal)
        bot_layout.addWidget(self.btn_normal)

        self.btn_charge = QPushButton("ŁADOWANIE\nMAGAZYNU")
        self.btn_charge.setCheckable(True)
        self.btn_group.addButton(self.btn_charge)
        bot_layout.addWidget(self.btn_charge)

        self.btn_discharge = QPushButton("WSPOMAGANIE\n(ROZŁADUNEK)")
        self.btn_discharge.setCheckable(True)
        self.btn_group.addButton(self.btn_discharge)
        bot_layout.addWidget(self.btn_discharge)

        bot_layout.addSpacing(40)

        self.btn_off = QPushButton("ODŁĄCZNIK\nGŁÓWNY")
        self.btn_off.setObjectName("btn_stop")
        self.btn_off.setCheckable(True)
        self.btn_group.addButton(self.btn_off)
        bot_layout.addWidget(self.btn_off)

        bot_layout.addStretch()
        main_layout.addWidget(self.frame_bot, stretch=1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_physics)
        self.timer.start(100)

    def update_physics(self):
        dt = 0.1

        mw_in = self.scene.Turbina.power_mw
        mw_out = 0.0

        active_bats = []
        if self.chk_a.isChecked(): active_bats.append(self.scene.bat1)
        if self.chk_b.isChecked(): active_bats.append(self.scene.bat2)

        if self.btn_normal.isChecked():
            mw_out = mw_in
            self.arrow_1.setText(">>>")
            self.arrow_1.setStyleSheet("color: #00ff00; font-size: 30px;")
            self.arrow_2.setText(">>>")
            self.arrow_2.setStyleSheet("color: #00ff00; font-size: 30px;")
            self.lbl_bat_status.setText("SPOCZYNEK")
            self.lbl_bat_status.setStyleSheet("color: gray;")

        elif self.btn_charge.isChecked():
            TOTAL_CHARGE_CAPACITY = 15.0

            if mw_in > 0 and len(active_bats) > 0:
                hungry = [b for b in active_bats if b.charge < 100.0]
                used = 0.0

                if hungry:
                    p_per_bat = TOTAL_CHARGE_CAPACITY / len(hungry)

                    if mw_in < TOTAL_CHARGE_CAPACITY:
                        p_per_bat = mw_in / len(hungry)
                        used = mw_in
                    else:
                        used = TOTAL_CHARGE_CAPACITY

                    for b in hungry:
                        b.charge += p_per_bat * 0.2 * dt
                        if b.charge > 100: b.charge = 100

                    self.lbl_bat_status.setText(f"ŁADOWANIE ({len(hungry)} SEKCJE)")
                    self.lbl_bat_status.setStyleSheet("color: orange; font-weight: bold;")
                else:
                    self.lbl_bat_status.setText("SEKCJE PEŁNE")
                    self.lbl_bat_status.setStyleSheet("color: green;")

                mw_out = max(0.0, mw_in - used)
            else:
                mw_out = 0.0
                if len(active_bats) == 0:
                    self.lbl_bat_status.setText("BRAK SEKCJI!")
                    self.lbl_bat_status.setStyleSheet("color: red;")
                else:
                    self.lbl_bat_status.setText("BRAK MOCY WEJ.")
                    self.lbl_bat_status.setStyleSheet("color: red;")

            self.arrow_1.setText(">>>")
            self.arrow_1.setStyleSheet("color: orange; font-size: 30px;")
            self.arrow_2.setText(">>>") if mw_out > 0 else self.arrow_2.setText("---")

        elif self.btn_discharge.isChecked():
            TOTAL_DISCHARGE_CAP = 20.0

            full = [b for b in active_bats if b.charge > 0.0]
            boost = 0.0

            if full:
                p_per_bat = TOTAL_DISCHARGE_CAP / len(full)
                for b in full:
                    b.charge -= p_per_bat * 0.25 * dt
                    if b.charge < 0: b.charge = 0
                    boost += p_per_bat

                self.lbl_bat_status.setText(f"ODDAWANIE ({len(full)} SEKCJE)")
                self.lbl_bat_status.setStyleSheet("color: cyan; font-weight: bold;")
                self.arrow_1.setText(">>>")
                self.arrow_1.setStyleSheet("color: #00ff00; font-size: 30px;")
                self.arrow_2.setText(">>> >>>")
                self.arrow_2.setStyleSheet("color: cyan; font-size: 30px;")
            else:
                if len(active_bats) == 0:
                    self.lbl_bat_status.setText("BRAK SEKCJI!")
                else:
                    self.lbl_bat_status.setText("PUSTE!")
                self.lbl_bat_status.setStyleSheet("color: red; font-weight: bold;")
                self.arrow_2.setText(">>>")

            mw_out = mw_in + boost

        elif self.btn_off.isChecked():
            mw_out = 0.0
            self.arrow_1.setText("X")
            self.arrow_1.setStyleSheet("color: red; font-size: 30px;")
            self.arrow_2.setText("X")
            self.arrow_2.setStyleSheet("color: red; font-size: 30px;")
            self.lbl_bat_status.setText("ODCIĘTE")
            self.lbl_bat_status.setStyleSheet("color: red;")

        self.lbl_gen.setText(f"{mw_in:.1f} MW")
        self.lbl_grid.setText(f"{mw_out:.1f} MW")
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Elektrociepłownia")
        self.resize(1100, 750)
        self.setStyleSheet("background-color: black;")

        self.scene = ScadaScene()
        self.setCentralWidget(self.scene)

        self.timer = QTimer()
        self.timer.timeout.connect(self.scene.update_simulation)
        self.timer.start(50)

        self.okno_materialy = None
        self.okno_gen = None
        self.okno_energy = None

        btn = QPushButton("Materiały", self)
        btn.setGeometry(50, 600, 200, 50)
        btn.setStyleSheet("background-color: lightgray; color: black; border: 2px solid white;")
        btn.clicked.connect(self.otworz_okno_materialy)

        btn_gen = QPushButton("Generacja", self)
        btn_gen.setGeometry(260, 600, 200, 50)
        btn_gen.setStyleSheet("background-color: lightgray; color: black; border: 2px solid white;")
        btn_gen.clicked.connect(self.otworz_okno_generacji)

        btn_en = QPushButton("Energia", self)
        btn_en.setGeometry(470, 600, 200, 50)
        btn_en.setStyleSheet("background-color: lightgray; color: black; border: 2px solid white;")
        btn_en.clicked.connect(self.otworz_okno_energii)

    def otworz_okno_materialy(self):
        if self.okno_materialy is None:
            self.okno_materialy = okno_materialy(self.scene)
        self.okno_materialy.show()

    def otworz_okno_generacji(self):
        if self.okno_gen is None:
            self.okno_gen = okno_generacja(self.scene)
        self.okno_gen.show()

    def otworz_okno_energii(self):
        if self.okno_energy is None:
            self.okno_energy = okno_energia(self.scene)
        self.okno_energy.show()

if __name__ == "__main__":
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())