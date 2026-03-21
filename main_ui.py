import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QDate


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(704, 878)
        # Global app styles: modern font and soft background gradient (Instagram-inspired accent)
        MainWindow.setStyleSheet("""
            /* Clean minimal global styles */
            QWidget { font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; color: #263238; }
            #centralwidget { background: #f4f7fb; }
            QGroupBox { background: white; border: 1px solid #e6eef6; border-radius: 8px; margin-top: 12px; }
            QLabel#lbl_admin_title { color: #4a148c; font-size: 24px; font-weight: 700; }
            QPushButton { background: #ffffff; border: 1px solid #d6e4ef; border-radius: 6px; padding: 6px 10px; }
            QPushButton#btn_refresh, QPushButton#btn_confirm { background: #1976d2; color: white; border: none; }
            QPushButton#btn_delete { background: #e53935; color: white; border: none; }
            QLineEdit, QComboBox, QDateEdit, QSpinBox, QPlainTextEdit { background: white; border: 1px solid #e1e7ee; border-radius: 6px; padding: 6px; }
        """)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setAutoFillBackground(False)
        self.centralwidget.setStyleSheet("#centralwidget {\n"
"    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, \n"
"                      stop:0 #ffffff, stop:1 #dfe4ea);\n"
"}")
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setAutoFillBackground(False)
        self.stackedWidget.setStyleSheet("background: transparent;")
        self.stackedWidget.setObjectName("stackedWidget")
        self.page_landing = QtWidgets.QWidget()
        self.page_landing.setStyleSheet("background: transparent;")
        self.page_landing.setObjectName("page_landing")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.page_landing)
        self.gridLayout_2.setObjectName("gridLayout_2")
        # Add vertical spacing so landing content sits near center
        try:
            self.gridLayout_2.setContentsMargins(0, 120, 0, 120)
        except Exception:
            pass
        # Place title and auth button directly on the landing page (no container)
        self.label = QtWidgets.QLabel(self.page_landing)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setObjectName("lbl_title")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)

        self.pushButton = QtWidgets.QPushButton(self.page_landing)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 1, 0, 1, 1, QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.stackedWidget.addWidget(self.page_landing)
        self.page_booking = QtWidgets.QWidget()
        self.page_booking.setStyleSheet("QGroupBox {\n"
    "    font-size: 14px;\n"
    "    font-weight: 700;\n"
    "    color: #2c3e50;\n"
    "    border: 1px solid #e6e9ee;\n"
    "    border-radius: 12px;\n"
    "    margin-top: 18px;\n"
    "    padding: 14px;\n"
    "    background-color: rgba(255,255,255,0.95);\n"
    "}\n"
    "\n"
    "QGroupBox::title {\n"
    "    subcontrol-origin: margin;\n"
    "    subcontrol-position: top left;\n"
    "    left: 12px;\n"
    "    padding: 0 6px;\n"
    "    color: #1f3a57;\n"
    "}\n"
    "\n"
    "QLineEdit, QComboBox, QDateEdit, QSpinBox, QPlainTextEdit {\n"
    "    border: 1px solid #d0d7df;\n"
    "    border-radius: 8px;\n"
    "    padding: 8px;\n"
    "    background-color: #ffffff;\n"
    "    color: #233042;\n"
    "    font-size: 14px;\n"
    "}\n"
    "\n"
    "QLineEdit:focus, QComboBox:focus, QDateEdit:focus {\n"
    "    border: 2px solid #3498db;\n"
    "    background-color: #fff;\n"
    "}\n"
    "\n"
    "QLabel {\n"
    "    font-size: 14px;\n"
    "    color: #2c3e50;\n"
    "}\n"
    "\n"
            "QPushButton#btn_confirm {\n"
"    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #4facfe, stop:1 #1f6fbf);\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"    font-weight: 700;\n"
"    min-height: 40px;\n"
"    padding: 10px 20px;\n"
"}\n"
"/* hover brightness removed for compatibility */\n"
    "\n"
    "QPushButton#btn_back {\n"
    "    background-color: transparent;\n"
    "    color: #2c3e50;\n"
    "    border: 1px solid #cfcfcf;\n"
    "    border-radius: 8px;\n"
    "    min-height: 36px;\n"
    "    padding: 8px 14px;\n"
    "}\n"
    "QPushButton#btn_back:hover {\n"
    "    background-color: #eaf2fb;\n"
    "}")
        self.page_booking.setObjectName("page_booking")
        self.gridLayout = QtWidgets.QGridLayout(self.page_booking)
        self.gridLayout.setContentsMargins(100, 50, 100, 50)
        self.gridLayout.setObjectName("gridLayout")
        self.btn_back = QtWidgets.QPushButton(self.page_booking)
        self.btn_back.setMaximumSize(QtCore.QSize(400, 16777215))
        self.btn_back.setStyleSheet("")
        self.btn_back.setObjectName("btn_back")
        self.gridLayout.addWidget(self.btn_back, 5, 0, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.page_booking)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMaximumSize(QtCore.QSize(400, 16777215))
        self.groupBox_3.setObjectName("groupBox_3")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox_3)
        self.formLayout.setObjectName("formLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox_3)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.input_name = QtWidgets.QLineEdit(self.groupBox_3)
        self.input_name.setObjectName("input_name")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.input_name)
        self.label_3 = QtWidgets.QLabel(self.groupBox_3)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.input_phone = QtWidgets.QLineEdit(self.groupBox_3)
        self.input_phone.setObjectName("input_phone")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.input_phone)
        self.label_4 = QtWidgets.QLabel(self.groupBox_3)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.input_email = QtWidgets.QLineEdit(self.groupBox_3)
        self.input_email.setObjectName("input_email")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.input_email)
        self.gridLayout.addWidget(self.groupBox_3, 0, 0, 1, 1)
        self.btn_confirm = QtWidgets.QPushButton(self.page_booking)
        self.btn_confirm.setMaximumSize(QtCore.QSize(400, 16777215))
        self.btn_confirm.setStyleSheet("")
        self.btn_confirm.setObjectName("btn_confirm")
        self.gridLayout.addWidget(self.btn_confirm, 4, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.page_booking)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setMaximumSize(QtCore.QSize(400, 16777215))
        self.groupBox.setObjectName("groupBox")
        self.formLayout_3 = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout_3.setObjectName("formLayout_3")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_8)
        self.spin_guests = QtWidgets.QSpinBox(self.groupBox)
        self.spin_guests.setObjectName("spin_guests")
        self.formLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.spin_guests)
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setObjectName("label_10")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_10)
        self.combo_payment = QtWidgets.QComboBox(self.groupBox)
        self.combo_payment.setObjectName("combo_payment")
        self.combo_payment.addItem("")
        self.combo_payment.addItem("")
        self.combo_payment.addItem("")
        self.combo_payment.addItem("")
        self.formLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.combo_payment)
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setObjectName("label_9")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_9)
        self.txt_requests = QtWidgets.QPlainTextEdit(self.groupBox)
        self.txt_requests.setObjectName("txt_requests")
        self.formLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.txt_requests)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout_3.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout)
        self.gridLayout.addWidget(self.groupBox, 2, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.page_booking)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setMaximumSize(QtCore.QSize(400, 16777215))
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout_2 = QtWidgets.QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_5 = QtWidgets.QLabel(self.groupBox_2)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_5)
        self.combo_room_type = QtWidgets.QComboBox(self.groupBox_2)
        self.combo_room_type.setObjectName("combo_room_type")
        self.combo_room_type.addItem("")
        self.combo_room_type.addItem("")
        self.combo_room_type.addItem("")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.combo_room_type)
        self.label_6 = QtWidgets.QLabel(self.groupBox_2)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_6)
        self.date_checkin = QtWidgets.QDateEdit(self.groupBox_2)
        self.date_checkin.setObjectName("date_checkin")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.date_checkin)
        self.label_7 = QtWidgets.QLabel(self.groupBox_2)
        self.label_7.setObjectName("label_7")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_7)
        self.date_checkout = QtWidgets.QDateEdit(self.groupBox_2)
        self.date_checkout.setObjectName("date_checkout")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.date_checkout)
        self.gridLayout.addWidget(self.groupBox_2, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 3, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_booking)
        self.page_admin = QtWidgets.QWidget()
        self.page_admin.setAutoFillBackground(False)
        self.page_admin.setStyleSheet(
            "QWidget#page_admin { background: transparent; }"
            "QTableWidget { background: white; border: none; gridline-color: #f0f3f6; }"
            "QTableWidget::item { padding: 6px; color: #263238; }"
            "QTableWidget::item:selected { background-color: #e8f3ff; }"
            "QHeaderView::section { background: transparent; color: #263238; font-size: 14px; padding: 8px; font-weight: 700; border-bottom: 1px solid #e6eef6; }"
        )
        self.page_admin.setObjectName("page_admin")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.page_admin)
        self.verticalLayout_3.setContentsMargins(18, 18, 18, 18)
        self.verticalLayout_3.setSpacing(12)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.header_frame = QtWidgets.QFrame(self.page_admin)
        self.header_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.header_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.header_frame.setObjectName("header_frame")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.header_frame)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.input_search = QtWidgets.QLineEdit(self.header_frame)
        self.input_search.setMinimumSize(QtCore.QSize(300, 0))
        self.input_search.setObjectName("input_search")
        self.horizontalLayout_2.addWidget(self.input_search)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.lbl_admin_title = QtWidgets.QLabel(self.header_frame)
        self.lbl_admin_title.setStyleSheet("/* --- ADMIN DASHBOARD TITLE --- */\n"
"QLabel#lbl_admin_title {\n"
"    color: #2c3e50;           /* Dark professional blue-grey */\n"
"    font-size: 24px;          /* Large enough to be a heading */\n"
"    font-weight: bold;        /* Makes it pop */\n"
"    font-family: \"Segoe UI\", sans-serif; /* Clean modern font */\n"
"    padding: 10px;            /* Gives it some space */\n"
"}")
        self.lbl_admin_title.setObjectName("lbl_admin_title")
        self.horizontalLayout_2.addWidget(self.lbl_admin_title)
        self.btn_logout = QtWidgets.QPushButton(self.header_frame)
        # Slightly larger button text for important controls
        try:
            font_btn = QtGui.QFont()
            font_btn.setPointSize(12)
            self.btn_confirm.setFont(font_btn)
            self.btn_back.setFont(font_btn)
            self.btn_logout.setFont(font_btn)
        except Exception:
            pass
        self.btn_logout.setObjectName("btn_logout")
        self.horizontalLayout_2.addWidget(self.btn_logout)
        self.verticalLayout_3.addWidget(self.header_frame)
        self.table_records = QtWidgets.QTableWidget(self.page_admin)
        self.table_records = QtWidgets.QTableWidget(self.page_admin)
        self.table_records.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table_records.setAlternatingRowColors(True)
        # Select entire rows (not individual cells) and allow single-row selection
        self.table_records.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.table_records.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_records.setShowGrid(False)
        self.table_records.setObjectName("table_records")
        self.table_records.setColumnCount(9)
        self.table_records.setRowCount(0)
        # Hide vertical row header to match desired layout
        try:
            self.table_records.verticalHeader().setVisible(False)
        except Exception:
            pass
        # Make columns stretch to fill available space and remove small focus outline for items
        try:
            header = self.table_records.horizontalHeader()
            # Prefer ResizeToContents for short columns and Stretch for name/room-type so text is readable
            header.setMinimumSectionSize(50)
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  # ID
            header.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)  # Username
            header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)          # Guest Name (main stretch)
            header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)          # Room Type (also stretches)
            header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents) # Guests
            header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents) # Check-in
            header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents) # Nights
            header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents) # Status
            header.setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeToContents) # Total Bill
            header.setStretchLastSection(False)
        except Exception:
            pass
        try:
            sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
            self.table_records.setSizePolicy(sizePolicy)
            self.table_records.setMinimumWidth(0)
        except Exception:
            pass
        try:
            # Increase table font and spacing for readability and remove focus outline
            self.table_records.setStyleSheet(
                "QTableWidget { font-size: 14px; }"
                "QHeaderView::section { background: transparent; color: #263238; font-size: 14px; padding: 8px; font-weight: 700; border-bottom: 1px solid #e6eef6; }"
                "QTableWidget::item:focus { outline: none; } QTableWidget:focus { outline: none; }"
            )
            try:
                # Slightly taller rows for clarity
                self.table_records.verticalHeader().setDefaultSectionSize(30)
            except Exception:
                pass
        except Exception:
            pass
        item = QtWidgets.QTableWidgetItem()
        self.table_records.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_records.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_records.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_records.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_records.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_records.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_records.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_records.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.table_records.setHorizontalHeaderItem(8, item)
        self.table_records.horizontalHeader().setStretchLastSection(True)
        # Add table with stretch so it expands to fill available space
        self.verticalLayout_3.addWidget(self.table_records, 1)
        self.footer_frame = QtWidgets.QFrame(self.page_admin)
        self.footer_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.footer_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.footer_frame.setObjectName("footer_frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.footer_frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.btn_refresh = QtWidgets.QPushButton(self.footer_frame)
        self.btn_refresh.setStyleSheet("/* --- REFRESH BUTTON (Normal State - Blue) --- */\n"
    "QPushButton#btn_refresh {\n"
    "    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #4facfe, stop:1 #1f6fbf);\n"
    "    color: white;\n"
    "    border: none;\n"
    "    border-radius: 4px;\n"
    "    padding: 8px 16px;\n"
    "    font-weight: bold;\n"
    "}\n"
    "\n"
    "/* REFRESH BUTTON (Hover State) */\n"
    "QPushButton#btn_refresh:hover {\n"
    "    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #3fa8ff, stop:1 #195fae);\n"
    "}\n"
    "\n"
    "/* REFRESH BUTTON (Pressed State) */\n"
    "QPushButton#btn_refresh:pressed {\n"
    "    background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #3aa6fb, stop:1 #1a61b8);\n"
    "}")
        self.btn_refresh.setObjectName("btn_refresh")
        self.horizontalLayout_3.addWidget(self.btn_refresh)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.btn_delete = QtWidgets.QPushButton(self.footer_frame)
        self.btn_delete.setStyleSheet("/* This is the normal state you already have */\n"
"QPushButton#btn_delete {\n"
"    background-color: #e74c3c; \n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    padding: 8px 16px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"/* --- ADD THIS PART FOR THE HOVER --- */\n"
"QPushButton#btn_delete:hover {\n"
"    background-color: #c0392b; /* A slightly darker red */\n"
"}\n"
"\n"
"/* Optional: This makes it even darker when you actually CLICK it */\n"
"QPushButton#btn_delete:pressed {\n"
"    background-color: #a93226;\n"
"}")
        self.btn_delete.setObjectName("btn_delete")
        self.horizontalLayout_3.addWidget(self.btn_delete)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem4)
        self.verticalLayout_3.addWidget(self.footer_frame)
        self.stackedWidget.addWidget(self.page_admin)
        self.verticalLayout_2.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 704, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Welcome to Hotel Reservation System"))
        self.pushButton.setText(_translate("MainWindow", "Login"))
        self.btn_back.setText(_translate("MainWindow", "Back to Home"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Guest Details"))
        self.label_2.setText(_translate("MainWindow", "Full Name"))
        self.label_3.setText(_translate("MainWindow", "Contact No."))
        self.label_4.setText(_translate("MainWindow", "Email"))
        self.btn_confirm.setText(_translate("MainWindow", "Confirm Booking"))
        self.groupBox.setTitle(_translate("MainWindow", "Preferences"))
        self.label_8.setText(_translate("MainWindow", "Number Of Guests"))
        self.label_10.setText(_translate("MainWindow", "Payment Method"))
        self.combo_payment.setItemText(0, _translate("MainWindow", "--Select Payment Method--"))
        self.combo_payment.setItemText(1, _translate("MainWindow", "Cash at Check-in"))
        self.combo_payment.setItemText(2, _translate("MainWindow", "Credit Card"))
        self.combo_payment.setItemText(3, _translate("MainWindow", "Debit Card"))
        self.label_9.setText(_translate("MainWindow", "Special Requests"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Stay Details"))
        self.label_5.setText(_translate("MainWindow", "Room Type"))
        self.combo_room_type.setItemText(0, _translate("MainWindow", "Standard - $100"))
        self.combo_room_type.setItemText(1, _translate("MainWindow", "Deluxe - $250"))
        self.combo_room_type.setItemText(2, _translate("MainWindow", "Suite - $500"))
        self.label_6.setText(_translate("MainWindow", "Check-in Date"))
        self.label_7.setText(_translate("MainWindow", "Check-out Date"))
        self.input_search.setPlaceholderText(_translate("MainWindow", "Search by Guest Name or ID"))
        self.lbl_admin_title.setText(_translate("MainWindow", "Admin Dashboard"))
        self.btn_logout.setText(_translate("MainWindow", "Logout"))
        item = self.table_records.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID"))
        item = self.table_records.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Username"))
        item = self.table_records.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Guest Name"))
        item = self.table_records.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Room Type"))
        item = self.table_records.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Guests"))
        item = self.table_records.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Check-in"))
        item = self.table_records.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Nights"))
        item = self.table_records.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Status"))
        item = self.table_records.horizontalHeaderItem(8)
        item.setText(_translate("MainWindow", "Total Bill"))
        self.btn_refresh.setText(_translate("MainWindow", "Refresh"))
        self.btn_delete.setText(_translate("MainWindow", "Delete"))
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        # Stub data for bookings
        self.bookings = []
        self.next_id = 1
        # Current user (simple placeholder). Replace with real auth when integrated.
        self.current_user = { 'username': 'guest' }
        
        # Connect signals
        self.connect_signals()
        
        # Start on landing page
        self.ui.stackedWidget.setCurrentIndex(0)

    def connect_signals(self):
        """Connect UI buttons to methods"""
        self.ui.pushButton.clicked.connect(self.show_login_dialog)
        self.ui.btn_back.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.btn_confirm.clicked.connect(self.confirm_booking)
        self.ui.btn_refresh.clicked.connect(self.on_refresh_clicked)
        self.ui.btn_delete.clicked.connect(self.delete_record)
        self.ui.input_search.textChanged.connect(self.filter_records)
        self.ui.btn_logout.clicked.connect(self.show_landing)

    def on_refresh_clicked(self):
        """Wrapper for refresh button to aid debugging and ensure records reload."""
        try:
            print("Refresh button clicked")
            self.load_records()
        except Exception as e:
            print(f"Error during refresh: {e}")

    def show_login_dialog(self):
        """Placeholder for login (TODO: integrate auth)"""
        print("Login clicked - TODO: show login dialog")
        self.ui.stackedWidget.setCurrentIndex(1)  # Go to booking for demo

    def show_register_dialog(self):
        """Placeholder for register"""
        print("Register clicked - TODO: show register dialog")

    def show_landing(self):
        """Show landing page"""
        self.ui.stackedWidget.setCurrentIndex(0)

    def confirm_booking(self):
        """Handle booking confirmation"""
        # Get form data
        name = self.ui.input_name.text()
        phone = self.ui.input_phone.text()
        email = self.ui.input_email.text()
        room_type = self.ui.combo_room_type.currentText()
        guests = self.ui.spin_guests.value()
        checkin = self.ui.date_checkin.date().toString("yyyy-MM-dd")
        checkout = self.ui.date_checkout.date().toString("yyyy-MM-dd")
        payment = self.ui.combo_payment.currentText()
        requests = self.ui.txt_requests.toPlainText()

        if not name or not phone or not room_type:
            print("Please fill required fields")
            return

        # Calculate nights and price
        nights = (self.ui.date_checkout.date() - self.ui.date_checkin.date()).days()
        if "Standard" in room_type:
            price_per_night = 100
        elif "Deluxe" in room_type:
            price_per_night = 250
        else:
            price_per_night = 500
        total = nights * price_per_night * guests

        booking = {
            "id": self.next_id,
            "username": self.current_user.get('username', 'guest'),
            "name": name,
            "phone": phone,
            "email": email,
            "room_type": room_type,
            "guests": guests,
            "checkin": checkin,
            "nights": nights,
            "status": "Confirmed",
            "total": f"${total:.2f}"
        }
        self.bookings.append(booking)
        self.next_id += 1

        print(f"Booking confirmed: {booking}")
        self.clear_booking_form()
        self.ui.stackedWidget.setCurrentIndex(2)  # Show admin to see booking
        self.load_records()

    def clear_booking_form(self):
        """Clear booking form"""
        self.ui.input_name.clear()
        self.ui.input_phone.clear()
        self.ui.input_email.clear()
        self.ui.combo_room_type.setCurrentIndex(0)
        self.ui.spin_guests.setValue(1)
        self.ui.date_checkin.setDate(QDate.currentDate())
        self.ui.date_checkout.setDate(QDate.currentDate().addDays(1))
        self.ui.combo_payment.setCurrentIndex(0)
        self.ui.txt_requests.clear()

    def load_records(self):
        """Load bookings into table"""
        self.ui.table_records.setRowCount(0)
        for booking in self.bookings:
            row = self.ui.table_records.rowCount()
            self.ui.table_records.insertRow(row)
            self.ui.table_records.setItem(row, 0, QtWidgets.QTableWidgetItem(str(booking["id"])))
            self.ui.table_records.setItem(row, 1, QtWidgets.QTableWidgetItem(booking.get("username", "guest")))
            self.ui.table_records.setItem(row, 2, QtWidgets.QTableWidgetItem(booking["name"]))
            self.ui.table_records.setItem(row, 3, QtWidgets.QTableWidgetItem(booking["room_type"]))
            self.ui.table_records.setItem(row, 4, QtWidgets.QTableWidgetItem(str(booking["guests"])))
            self.ui.table_records.setItem(row, 5, QtWidgets.QTableWidgetItem(booking["checkin"]))
            self.ui.table_records.setItem(row, 6, QtWidgets.QTableWidgetItem(str(booking["nights"])))
            self.ui.table_records.setItem(row, 7, QtWidgets.QTableWidgetItem(booking["status"]))
            self.ui.table_records.setItem(row, 8, QtWidgets.QTableWidgetItem(booking["total"]))

    def delete_record(self):
        """Delete selected record"""
        selection = self.ui.table_records.selectedItems()
        if selection:
            row = selection[0].row()
            booking_id = int(self.ui.table_records.item(row, 0).text())
            self.bookings = [b for b in self.bookings if b["id"] != booking_id]
            self.ui.table_records.removeRow(row)
            print(f"Deleted booking {booking_id}")

    def filter_records(self):
        """Filter table by search"""
        search = self.ui.input_search.text().lower()
        for row in range(self.ui.table_records.rowCount()):
            match = False
            for col in range(self.ui.table_records.columnCount()):
                item = self.ui.table_records.item(row, col)
                if item and search in item.text().lower():
                    match = True
                    break
            self.ui.table_records.setRowHidden(row, not match)

def show_page_booking(self):
    self.ui.stackedWidget.setCurrentIndex(1)

def show_page_admin(self):
    self.ui.stackedWidget.setCurrentIndex(2)
    self.load_records()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())



