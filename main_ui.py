from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(704, 878)
MainWindow.setStyleSheet("")
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
        self.landing_frame = QtWidgets.QFrame(self.page_landing)
        self.landing_frame.setMaximumSize(QtCore.QSize(400, 300))
        self.landing_frame.setStyleSheet("#landing_frame {\n"
"    background-color: rgba(255, 255, 255, 220); /* White with 85% opacity */\n"
"    border-radius: 15px;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background-color: #2c3e50;\n"
"    color: white;\n"
"    border-radius: 10px;\n"
"    padding: 12px;\n"
"    font-size: 14px;\n"
"    transition: background-color 0.3s;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background-color: #34495e;\n"
"    border: 2px solid #3498db;\n"
"}")
        self.landing_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.landing_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.landing_frame.setObjectName("landing_frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.landing_frame)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.landing_frame)
        font = QtGui.QFont()
        font.setPointSize(19)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setAutoFillBackground(False)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label, 0, QtCore.Qt.AlignHCenter)
        self.pushButton = QtWidgets.QPushButton(self.landing_frame)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(self.landing_frame)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.gridLayout_2.addWidget(self.landing_frame, 0, 0, 1, 1)
        self.stackedWidget.addWidget(self.page_landing)
        self.page_booking = QtWidgets.QWidget()
        self.page_booking.setStyleSheet("QGroupBox {\n"
"    font-size: 14px;\n"
"    font-weight: bold;\n"
"    color: #000000;\n"
"    border: 2px solid #dcdde1;\n"
"    border-radius: 10px;\n"
"    margin-top: 20px;\n"
"    padding: 10px;\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #dcdde1;\n"
"    border-radius: 15px;\n"
"    padding: 20px;\n"
"}\n"
"\n"
"QGroupBox::title {\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 15px;\n"
"    padding: 0 5px;\n"
"}\n"
"\n"
"/* Style all Input Fields (LineEdits, Combo Boxes, and DateEdits) */\n"
"QLineEdit, QComboBox, QDateEdit, QSpinBox, QPlainTextEdit {\n"
"    border: 1px solid #ced4da;\n"
"    border-radius: 5px;\n"
"    padding: 5px;\n"
"    background-color: #f8f9fa;\n"
"    color: #333;\n"
"    font-size: 13px;\n"
"}\n"
"\n"
"QLineEdit:focus, QComboBox:focus, QDateEdit:focus {\n"
"    border: 2px solid #3498db; /* Blue glow when typing */\n"
"    background-color: #fff;\n"
"}\n"
"\n"
"/* Style the Labels */\n"
"QLabel {\n"
"    font-size: 13px;\n"
"    color: #34495e;\n"
"    font-weight: normal;\n"
"}\n"
"\n"
"/* The Confirm Button */\n"
"QPushButton#btn_confirm {\n"
"    background-color: #27ae60;\n"
"    color: white;\n"
"    border-radius: 6px;\n"
"    font-weight: bold;\n"
"    min-height: 35px;\n"
"}\n"
"\n"
"/* THE HOVER - Make sure there is NO space between the name and the colon */\n"
"QPushButton#btn_confirm:hover {\n"
"    background-color: #2ecc71; /* A lighter green */\n"
"}\n"
"\n"
"/* The Back Button */\n"
"QPushButton#btn_back {\n"
"    background-color: rgba(255, 255, 255, 0.2); \n"
"    color: #c0392b;\n"
"    border: 1px solid #c0392b;\n"
"    border-radius: 6px;\n"
"    min-height: 35px;\n"
"}\n"
"\n"
"QPushButton#btn_back:hover {\n"
"    background-color: #c0392b;\n"
"    color: white;\n"
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
        self.page_admin.setStyleSheet("/* Background of the Admin Page */\n"
"QWidget#page_admin {\n"
"    background-color: #f4f7f6;\n"
"}\n"
"\n"
"/* Table Design */\n"
"QTableWidget {\n"
"    background-color: white;\n"
"    border: 1px solid #dcdfe3;\n"
"    gridline-color: #f0f0f0;\n"
"    border-radius: 5px;\n"
"}\n"
"\n"
"QHeaderView::section {\n"
"    background-color: #34495e;\n"
"    color: white;\n"
"    padding: 6px;\n"
"    font-weight: bold;\n"
"    border: none;\n"
"}\n"
"\n"
"/* Common Button Settings */\n"
"QPushButton {\n"
"    border-radius: 4px;\n"
"    padding: 8px 16px;\n"
"    font-weight: bold;\n"
"    font-size: 12px;\n"
"}\n"
"\n"
"/* --- REFRESH BUTTON (Green) --- */\n"
"QPushButton#btn_refresh {\n"
"    background-color: #27ae60;\n"
"    color: white;\n"
"    border: none;\n"
"}\n"
"QPushButton#btn_refresh:hover {\n"
"    background-color: #2ecc71;\n"
"}\n"
"\n"
"/* --- DELETE BUTTON (Red) --- */\n"
"QPushButton#btn_delete {\n"
"    background-color: #e74c3c;\n"
"    color: white;\n"
"    border: none;\n"
"}\n"
"QPushButton#btn_delete:hover {\n"
"    background-color: #ff5e4d;\n"
"}\n"
"\n"
"/* --- LOGOUT BUTTON (Dark Grey/Professional) --- */\n"
"QPushButton#btn_logout {\n"
"    background-color: #95a5a6;\n"
"    color: white;\n"
"    border: none;\n"
"}\n"
"QPushButton#btn_logout:hover {\n"
"    background-color: #7f8c8d;\n"
"}\n"
"\n"
"/* Search Bar Styling */\n"
"QLineEdit {\n"
"    border: 1px solid #bdc3c7;\n"
"    border-radius: 4px;\n"
"    padding: 5px;\n"
"    background-color: white;\n"
"}\n"
"\n"
"/* Table Header Styling */\n"
"QHeaderView::section {\n"
"    background-color: #1a1a1a; /* Matches your Black title vibe */\n"
"    color: white;\n"
"    padding: 8px;\n"
"    font-weight: bold;\n"
"    border: none;\n"
"    border-right: 1px solid #333; /* Subtle divider */\n"
"}\n"
"\n"
"/* Make the Total Bill column bold */\n"
"QTableWidget::item {\n"
"    padding: 5px;\n"
"}\n"
"\n"
"/* Highlight the last column (Total Bill) */\n"
"QTableWidget::item:last-child {\n"
"    font-weight: bold;\n"
"    color: #27ae60; /* Money green */\n"
"}\n"
"\n"
"/* LOGOUT BUTTON (Normal) */\n"
"QPushButton#btn_logout {\n"
"    background-color: #7f8c8d; /* Professional Slate Grey */\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    padding: 5px 15px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"/* LOGOUT BUTTON (Hover) */\n"
"QPushButton#btn_logout:hover {\n"
"    background-color: #95a5a6; /* Lighter grey so it \"lights up\" */\n"
"}\n"
"\n"
"/* LOGOUT BUTTON (Pressed) */\n"
"QPushButton#btn_logout:pressed {\n"
"    background-color: #2c3e50; /* Deep blue-grey when clicked */\n"
"}")
        self.page_admin.setObjectName("page_admin")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.page_admin)
        self.verticalLayout_3.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout_3.setSpacing(15)
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
        self.btn_logout.setObjectName("btn_logout")
        self.horizontalLayout_2.addWidget(self.btn_logout)
        self.verticalLayout_3.addWidget(self.header_frame)
        self.table_records = QtWidgets.QTableWidget(self.page_admin)
        self.table_records.setFocusPolicy(QtCore.Qt.NoFocus)
        self.table_records.setAlternatingRowColors(True)
        self.table_records.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.table_records.setShowGrid(False)
        self.table_records.setObjectName("table_records")
        self.table_records.setColumnCount(8)
        self.table_records.setRowCount(0)
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
        self.table_records.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_3.addWidget(self.table_records)
        self.footer_frame = QtWidgets.QFrame(self.page_admin)
        self.footer_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.footer_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.footer_frame.setObjectName("footer_frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.footer_frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.btn_refresh = QtWidgets.QPushButton(self.footer_frame)
        self.btn_refresh.setStyleSheet("/* --- REFRESH BUTTON (Normal State - Green) --- */\n"
"QPushButton#btn_refresh {\n"
"    background-color: #27ae60; /* Emerald Green */\n"
"    color: white;\n"
"    border: none;\n"
"    border-radius: 4px;\n"
"    padding: 8px 16px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"/* REFRESH BUTTON (Hover State - Lighter Green) */\n"
"QPushButton#btn_refresh:hover {\n"
"    background-color: #2ecc71; /* Brighter Green */\n"
"}\n"
"\n"
"/* REFRESH BUTTON (Pressed State - Darker Green) */\n"
"QPushButton#btn_refresh:pressed {\n"
"    background-color: #1e8449;\n"
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
        self.label.setText(_translate("MainWindow", "HOTEL RESERVATION SYSTEM"))
        self.pushButton.setText(_translate("MainWindow", "Booking"))
        self.pushButton_2.setText(_translate("MainWindow", "Admin Login"))
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
        item.setText(_translate("MainWindow", "Guest Name"))
        item = self.table_records.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Room Type"))
        item = self.table_records.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Guests"))
        item = self.table_records.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Check-in"))
        item = self.table_records.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Nights"))
        item = self.table_records.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "Status"))
        item = self.table_records.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "Total Bill"))
        self.btn_refresh.setText(_translate("MainWindow", "Refresh"))
        self.btn_delete.setText(_translate("MainWindow", "Delete"))
# import resources_rc  # Commented out since no resources.qrc exists
