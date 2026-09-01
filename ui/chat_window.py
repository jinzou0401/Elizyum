import threading

from PySide6.QtCore import QObject, Qt, Signal
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QMainWindow, QMessageBox, QPushButton, QScrollArea, QTextEdit,
    QVBoxLayout, QWidget)

P = {"bg":"#EEF6FF","side":"#F7FBFF","white":"#FFFFFF","line":"#CFE1F5",
     "text":"#112D4E","muted":"#607D9D","blue":"#4A90E2","user":"#E4F0FF",
     "eli":"#F080A4","eli_bg":"#FFE0EA","eli_text":"#7A2948",
     "aurora":"#42C98A","aurora_bg":"#DDF8E9","aurora_text":"#17623B"}


class Input(QTextEdit):
    enviar = Signal()
    def keyPressEvent(self, e):
        if e.key() in (Qt.Key_Return, Qt.Key_Enter) and not e.modifiers() & Qt.ShiftModifier:
            self.enviar.emit(); return
        super().keyPressEvent(e)


class Bridge(QObject):
    individual = Signal(str)
    grupo = Signal(object)
    error = Signal(str)


class ChatWindow(QMainWindow):
    def __init__(self, motores, nombre="eli"):
        super().__init__()
        self.motores, self.nombre = motores, nombre.lower()
        self.motor = motores[self.nombre]
        self.bridge = Bridge()
        self.bridge.individual.connect(self._fin_individual)
        self.bridge.grupo.connect(self._fin_grupo)
        self.bridge.error.connect(self._error)
        self.resize(1180, 780); self.setMinimumSize(920, 620)
        self._crear(); self._historial()

    def _crear(self):
        root=QWidget(); root.setObjectName("root"); self.setCentralWidget(root)
        shell=QHBoxLayout(root); shell.setContentsMargins(0,0,0,0); shell.setSpacing(0)
        side=QFrame(); side.setObjectName("side"); side.setFixedWidth(250)
        sl=QVBoxLayout(side); sl.setContentsMargins(22,26,22,24); sl.setSpacing(10)
        brand=QLabel("◜  E L I Z Y U M"); brand.setObjectName("brand"); sl.addWidget(brand); sl.addSpacing(30)
        self.nav={}
        for key,text in (("eli","✦   Eli"),("aurora","●   Aurora"),("grupo","◉   Grupo")):
            b=QPushButton(text); b.setObjectName("nav"); b.setCursor(Qt.PointingHandCursor)
            b.clicked.connect(lambda checked=False,n=key:self.cambiar_motor(n)); sl.addWidget(b); self.nav[key]=b
        sl.addStretch()
        nuevo=QPushButton("⊕   Nueva conversación"); nuevo.setObjectName("secondary")
        nuevo.clicked.connect(self.nueva_conversacion); sl.addWidget(nuevo)
        ajustes=QPushButton("⚙   Ajustes"); ajustes.setObjectName("secondary"); sl.addWidget(ajustes)
        shell.addWidget(side)

        main=QFrame(); main.setObjectName("main"); ml=QVBoxLayout(main)
        ml.setContentsMargins(30,24,30,22); ml.setSpacing(14)
        head=QHBoxLayout(); self.avatar=QLabel(); self.avatar.setAlignment(Qt.AlignCenter); self.avatar.setFixedSize(68,68)
        head.addWidget(self.avatar); titles=QVBoxLayout(); titles.setSpacing(2)
        self.title=QLabel(); self.title.setObjectName("title"); self.status=QLabel(); titles.addWidget(self.title); titles.addWidget(self.status)
        head.addLayout(titles); head.addStretch(); ml.addLayout(head)
        self.scroll=QScrollArea(); self.scroll.setObjectName("scroll"); self.scroll.setWidgetResizable(True); self.scroll.setFrameShape(QFrame.NoFrame)
        self.chat=QWidget(); self.chat.setObjectName("chat"); self.messages=QVBoxLayout(self.chat)
        self.messages.setContentsMargins(16,16,16,16); self.messages.setSpacing(12); self.messages.addStretch()
        self.scroll.setWidget(self.chat); ml.addWidget(self.scroll,1)
        card=QFrame(); card.setObjectName("inputCard"); il=QHBoxLayout(card); il.setContentsMargins(18,10,10,10)
        self.input=Input(); self.input.setObjectName("input"); self.input.setPlaceholderText("Escribe un mensaje..."); self.input.setFixedHeight(72)
        self.input.enviar.connect(self.enviar_mensaje); il.addWidget(self.input,1)
        self.send=QPushButton("➤"); self.send.setFixedSize(52,52); self.send.clicked.connect(self.enviar_mensaje); il.addWidget(self.send)
        ml.addWidget(card); shell.addWidget(main,1)
        self.setStyleSheet(self._qss()); self._identidad()

    def _qss(self):
        return f'''QWidget#root,QFrame#main{{background:{P['bg']};}} QFrame#side{{background:{P['side']};border-right:1px solid {P['line']};}}
        QLabel#brand{{color:{P['text']};font:700 17px "Segoe UI";}} QLabel#title{{color:{P['text']};font:700 32px "Segoe UI";}}
        QPushButton#nav,QPushButton#secondary{{background:transparent;color:{P['text']};border:1px solid transparent;border-radius:14px;padding:14px 16px;text-align:left;font:15px "Segoe UI";}}
        QPushButton#nav:hover{{background:{P['user']};border-color:{P['line']};}} QPushButton#secondary{{background:white;border-color:{P['line']};}}
        QScrollArea#scroll,QWidget#chat{{background:#FBFDFF;}} QScrollArea#scroll{{border:1px solid {P['line']};border-radius:20px;}}
        QFrame#inputCard{{background:white;border:1px solid {P['blue']};border-radius:20px;}} QTextEdit#input{{background:transparent;color:{P['text']};border:0;font:15px "Segoe UI";}}
        QScrollBar:vertical{{background:transparent;width:8px;}} QScrollBar::handle:vertical{{background:#BDD3EA;border-radius:4px;min-height:30px;}}'''

    def cambiar_motor(self,nombre):
        if nombre==self.nombre:return
        self.nombre=nombre; self.motor=self.motores[nombre]; self._identidad(); self._limpiar(); self._historial()

    def _identidad(self):
        data={"eli":("Eli","E",P["eli"],P["eli_bg"],P["eli_text"],"Cercana · conectada"),
              "aurora":("Aurora","A",P["aurora"],P["aurora_bg"],P["aurora_text"],"Creativa · conectada"),
              "grupo":("Grupo","E+A",P["blue"],"#F1EBF8",P["text"],"Eli y Aurora · conectadas")}
        title,letter,accent,soft,text,status=data[self.nombre]; self.setWindowTitle(f"Elizyum — {title}")
        self.title.setText(title); self.avatar.setText(letter); self.status.setText(f"●  {status}")
        self.avatar.setStyleSheet(f"background:{accent};color:white;border-radius:34px;font:700 19px 'Segoe UI';")
        self.status.setStyleSheet(f"color:{accent};font:14px 'Segoe UI';")
        self.send.setStyleSheet(f"background:{accent};color:white;border:0;border-radius:26px;font:700 22px 'Segoe UI';")
        for n,b in self.nav.items():
            b.setStyleSheet(f"background:{soft};color:{text};border:1px solid {accent};border-radius:14px;padding:14px 16px;text-align:left;font:600 15px 'Segoe UI';" if n==self.nombre else "")

    def _limpiar(self):
        while self.messages.count()>1:
            item=self.messages.takeAt(0)
            if item.widget():item.widget().deleteLater()

    def _historial(self):
        history=getattr(self.motor,"historial_grupo",[]) if self.nombre=="grupo" else getattr(self.motor,"messages",[])
        for m in history:
            if m.get("role")=="user": self.mostrar("Tú",m.get("content",""))
            elif m.get("role")=="assistant": self.mostrar(m.get("member",self.nombre).capitalize(),m.get("content",""))

    def mostrar(self,autor,mensaje):
        key=autor.lower(); ai=key in ("eli","aurora","elizyum"); row=QFrame(); rl=QHBoxLayout(row); rl.setContentsMargins(8,2,8,2)
        if not ai:rl.addStretch()
        bubble=QFrame(); bubble.setMaximumWidth(650); bl=QVBoxLayout(bubble); bl.setContentsMargins(16,12,16,12)
        who=QLabel(autor); who.setStyleSheet("font:700 12px 'Segoe UI';background:transparent;")
        text=QLabel(str(mensaje)); text.setWordWrap(True); text.setTextInteractionFlags(Qt.TextSelectableByMouse); text.setStyleSheet("font:15px 'Segoe UI';background:transparent;")
        bl.addWidget(who);bl.addWidget(text)
        if key=="aurora":bg,fg=P["aurora_bg"],P["aurora_text"]
        elif key in ("eli","elizyum"):bg,fg=P["eli_bg"],P["eli_text"]
        else:bg,fg=P["user"],P["text"]
        bubble.setStyleSheet(f"QFrame{{background:{bg};color:{fg};border-radius:18px;}}")
        rl.addWidget(bubble)
        if ai:rl.addStretch()
        self.messages.insertWidget(self.messages.count()-1,row); QApplication.processEvents(); self.scroll.verticalScrollBar().setValue(self.scroll.verticalScrollBar().maximum())

    def enviar_mensaje(self):
        msg=self.input.toPlainText().strip()
        if not msg:return
        self.input.clear();self.mostrar("Tú",msg)
        if self.nombre!="grupo":
            cmd=self.motor.procesar_comando(msg)
            if cmd!="no_es_comando":
                if cmd:self.mostrar(self.nombre.capitalize(),cmd)
                return
            try:self.motor.analizar_y_actualizar_emociones(msg);self.motor.registrar_mensaje_usuario(msg)
            except Exception as e:self._error(str(e));return
        self.send.setEnabled(False);self.status.setText("●  Pensando...")
        threading.Thread(target=self._worker,args=(msg,self.nombre,self.motor),daemon=True).start()

    def _worker(self,msg,nombre,motor):
        try:
            if nombre=="grupo":self.bridge.grupo.emit(motor.enviar_mensaje(msg))
            else:self.bridge.individual.emit(motor.obtener_respuesta())
        except Exception as e:self.bridge.error.emit(str(e))

    def _fin_individual(self,r):self.mostrar(self.nombre.capitalize(),r);self.send.setEnabled(True);self._identidad()
    def _fin_grupo(self,rs):
        for n,r in rs.items():self.mostrar(n.capitalize(),r)
        self.send.setEnabled(True);self._identidad()
    def _error(self,e):self.mostrar("Elizyum",f"No pude completar la respuesta.\n\nError: {e}");self.send.setEnabled(True);self._identidad()

    def nueva_conversacion(self):
        names={"eli":"Eli","aurora":"Aurora","grupo":"el grupo"}
        if QMessageBox.question(self,"Nueva conversación",f"¿Quieres comenzar una nueva conversación con {names[self.nombre]}?")!=QMessageBox.Yes:return
        if self.nombre=="grupo":self.motor.historial_grupo=[]
        else:self.motor.nueva_conversacion()
        self._limpiar();self._identidad()
