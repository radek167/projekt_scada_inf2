import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QLabel, QHBoxLayout, QSlider, QFrame
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
        self.flow_in = 0.0  # Otwarcie zaworu wlotowego
        self.flow_out = 0.0  # Otwarcie zaworu wylotowego
        self.ui_label_m3 = None  # Miejsce na etykietę licznika

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

    def draw_content(self, painter):
        painter.setPen(QPen(QColor(255, 100, 100), 2))
        painter.setBrush(QColor(60, 0, 0))
        painter.drawRect(0, 0, int(self.width), int(self.height))

        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 9))
        painter.drawText(10, 30, "REZERWA")
        painter.drawText(10, 50, "GORĄCEJ")
        painter.drawText(10, 70, "WODY")


class Bateria(Scada):
    def __init__(self, x, y, name):
        Scada.__init__(self, x, y, 100, 140, name)
        self.charge = 50.0

    def update(self, dt):
        if self.charge < 100: self.charge += 5.0 * dt

    def draw_content(self, painter):
        painter.setPen(QPen(Qt.white, 2))
        painter.setBrush(Qt.NoBrush)
        painter.drawRect(0, 0, int(self.width), int(self.height))

        margin_x = 10
        active_height = self.height - 40
        fill_h = (self.charge / 100.0) * active_height

        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(0, 255, 0) if self.charge > 20 else QColor(255, 0, 0))
        painter.drawRect(QRectF(margin_x, self.height - 30 - fill_h, self.width - 2 * margin_x, fill_h))

        painter.setPen(Qt.white)
        painter.setFont(QFont("Arial", 9))
        painter.drawText(5, -10, self.name)
        painter.drawText(30, int(self.height) - 5, f"{int(self.charge)}%")


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
        self.Ruras.append(Rura(490, 430, 600, 430, QColor(255, 100, 100), 4, "MIASTO"))

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

        lbl_woda = QLabel("STEROWNIA HYDRAULICZNA (1000 m³)")
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

        btn = QPushButton("Materiały", self)
        btn.setGeometry(50,600,200,50)
        btn.setStyleSheet("background-color: lightgray; color: black; border: 2px solid white;")
        btn.clicked.connect(self.okno_materialy1)

    def okno_materialy1(self):
        if self.okno_materialy is None:
            self.okno_materialy = okno_materialy(self.scene)

        self.okno_materialy.show()

if __name__ == "__main__":
    if hasattr(Qt, 'AA_EnableHighDpiScaling'):
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
        QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())