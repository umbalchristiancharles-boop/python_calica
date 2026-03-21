from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if hasattr(self, 'centralwidget'):
            return  # Already setup
        
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1100, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_2.setSpacing(10)
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setStyleSheet("""
            QStackedWidget { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
            stop:0 #e3f2fd, stop:1 #bbdefb); }
        """)
        self.stackedWidget.setObjectName("stackedWidget")
        
        self.setup_page_landing()
        self.setup_page_auth()
        self.setup_page_booking()
        self.setup_page_admin()
        
        self.verticalLayout_2.addWidget(self.stackedWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setup_page_landing(self):
        """Page 0: Landing page."""
        self.page_landing = QtWidgets.QWidget()
        self.page_landing.setObjectName("page_landing")
        layout = QtWidgets.QVBoxLayout(self.page_landing)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        
        title = QtWidgets.QLabel()
        title.setText("Welcome to Hotel Reservation System")
        title.setFont(QtGui.QFont("Segoe UI", 28, QtGui.QFont.Bold))
        title.setStyleSheet("color: #2c3e50; margin: 40px; padding: 20px;")
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)
        
        frame = QtWidgets.QFrame()
        frame.setFixedSize(400, 250)
        frame.setStyleSheet("""
            #frame { background: rgba(255,255,255,0.95); border-radius: 20px; 
            border: 3px solid #3498db; box-shadow: 0 8px 32px rgba(0,0,0,0.1); }
        """)
        frame.setObjectName("frame")
        frame_layout = QtWidgets.QVBoxLayout(frame)
        frame_layout.setSpacing(20)
        frame_layout.setContentsMargins(40, 40, 40, 40)
        
        # Clear, readable booking button with tooltip and accessibility name
        self.pushButton_booking = QtWidgets.QPushButton("📅  Quick Booking (Guest)")
        self.pushButton_booking.setObjectName("pushButton_booking")
        font = QtGui.QFont("Segoe UI", 15)
        font.setBold(True)
        self.pushButton_booking.setFont(font)
        # Strong contrast gradient and light border for readability
        self.pushButton_booking.setStyleSheet("""
            QPushButton {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #2b80d9, stop:1 #1b6fb3);
                color: #ffffff;
                border: 2px solid rgba(255,255,255,0.18);
                border-radius: 12px;
                padding: 14px 20px;
                font-size: 15px;
            }
            QPushButton:hover {
                background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:0 #1f6fb3, stop:1 #265d9a);
            }
        """)
        self.pushButton_booking.setMinimumHeight(64)
        self.pushButton_booking.setMinimumWidth(320)
        self.pushButton_booking.setCursor(QtCore.Qt.PointingHandCursor)
        self.pushButton_booking.setToolTip("Quick booking as guest — no account required")
        self.pushButton_booking.setAccessibleName("QuickBookingButton")
        self.pushButton_booking.setAutoDefault(False)
        frame_layout.addWidget(self.pushButton_booking, alignment=QtCore.Qt.AlignCenter)
        
        self.pushButton_auth = QtWidgets.QPushButton("🔐 Login / Register")
        self.pushButton_auth.setObjectName("pushButton_auth")
        self.pushButton_auth.setFont(QtGui.QFont("Segoe UI", 14))
        self.pushButton_auth.setStyleSheet("""
            QPushButton { background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #f39c12, stop:1 #e67e22);
                        color: #ffffff; border-radius: 12px; padding: 15px; }
            QPushButton:hover { background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #e67e22, stop:1 #f39c12); }
        """)
        self.pushButton_auth.setMinimumHeight(60)
        self.pushButton_auth.setMinimumWidth(300)
        self.pushButton_auth.setCursor(QtCore.Qt.PointingHandCursor)
        frame_layout.addWidget(self.pushButton_auth, alignment=QtCore.Qt.AlignCenter)
        
        layout.addWidget(frame, alignment=QtCore.Qt.AlignCenter)
        self.stackedWidget.addWidget(self.page_landing)

    def setup_page_auth(self):
        """Page 1: Auth (login/register tabs)."""
        self.page_auth = QtWidgets.QWidget()
        self.page_auth.setObjectName("page_auth")
        layout = QtWidgets.QVBoxLayout(self.page_auth)
        layout.setContentsMargins(100, 50, 100, 50)
        layout.setSpacing(25)
        
        frame = QtWidgets.QFrame()
        frame.setMaximumWidth(500)
        frame.setStyleSheet("""
            background: qlineargradient(to bottom, white, #f8f9fa); 
            border-radius: 25px; border: 3px solid #3498db; 
            box-shadow: 0 10px 30px rgba(52,152,219,0.3);
            QLineEdit {
                color: #333333;
                padding: 12px;
                border: 2px solid #dddddd;
                border-radius: 8px;
                background-color: white;
                font-size: 14px;
                min-height: 20px;
            }
            QLineEdit:focus {
                border-color: #3498db;
                background-color: #f8f9ff;
            }
            QLineEdit::placeholderText {
                color: #6c7a89;
                font-style: italic;
                font-size: 13px;
            }
            QLineEdit[echoMode="2"]::placeholderText {
                color: #999999;
            }
        """)
        frame_layout = QtWidgets.QVBoxLayout(frame)
        frame_layout.setSpacing(20)
        frame_layout.setContentsMargins(40, 40, 40, 40)
        
        title = QtWidgets.QLabel("🔐 Access Your Account")
        title.setObjectName("label_auth_title")
        title.setFont(QtGui.QFont("Segoe UI", 22, QtGui.QFont.Bold))
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("color: #3498db; margin: 10px;")
        frame_layout.addWidget(title)
        
        self.tabWidget_auth = QtWidgets.QTabWidget(frame)
        
        # Login Tab
        tab_login = QtWidgets.QWidget()
        tab_login_layout = QtWidgets.QVBoxLayout(tab_login)
        tab_login_layout.setSpacing(15)
        tab_login_layout.setContentsMargins(30, 30, 30, 30)
        
        QtWidgets.QLabel("Username:").setObjectName("label_login_user")
        self.input_login_user = QtWidgets.QLineEdit(placeholderText="Username (e.g. admin)")
        self.input_login_user.setObjectName("input_login_user")
        self.input_login_user.setClearButtonEnabled(True)
        tab_login_layout.addWidget(self.input_login_user)
        
        QtWidgets.QLabel("Password:").setObjectName("label_login_pw")
        self.input_login_pw = QtWidgets.QLineEdit()
        self.input_login_pw.setEchoMode(QtWidgets.QLineEdit.Password)
        self.input_login_pw.setPlaceholderText("Password (e.g. Admin@123)")
        self.input_login_pw.setObjectName("input_login_pw")
        self.input_login_pw.setClearButtonEnabled(True)
        tab_login_layout.addWidget(self.input_login_pw)
        
        self.btn_login = QtWidgets.QPushButton("Login")
        self.btn_login.setObjectName("btn_login")
        self.btn_login.setStyleSheet("background: #3498db; color: white; font-size: 16px; min-height: 50px; border-radius: 10px;")
        tab_login_layout.addWidget(self.btn_login)
        self.tabWidget_auth.addTab(tab_login, "Login")
        
        # Register Tab (similar)
        tab_register = QtWidgets.QWidget()
        tab_reg_layout = QtWidgets.QVBoxLayout(tab_register)
        tab_reg_layout.setSpacing(12)
        tab_reg_layout.setContentsMargins(30, 30, 30, 30)
        
        labels = ["Full Name:", "Username:", "Email:", "Phone:", "Password:"]
        fields = ["input_reg_name", "input_reg_user", "input_reg_email", "input_reg_phone", "input_reg_pw"]
        placeholders = ["e.g. Juan Dela Cruz", "choose a username", "you@example.com", "09171234567", "Create a password (6+)"]
        
        for label_text, field_name, ph in zip(labels, fields, placeholders):
            lbl = QtWidgets.QLabel(label_text)
            lbl.setObjectName(f"label_reg_{field_name.split('_')[-1]}")
            inp = QtWidgets.QLineEdit()
            inp.setPlaceholderText(ph)
            inp.setObjectName(field_name)
            inp.setClearButtonEnabled(True)
            if 'pw' in field_name:
                inp.setEchoMode(QtWidgets.QLineEdit.Password)
            tab_reg_layout.addWidget(lbl)
            tab_reg_layout.addWidget(inp)
            setattr(self, field_name, inp)
        
        self.btn_register = QtWidgets.QPushButton("Create Account")
        self.btn_register.setObjectName("btn_register")
        self.btn_register.setStyleSheet("background: #f39c12; color: white; font-size: 16px; min-height: 50px; border-radius: 10px;")
        tab_reg_layout.addWidget(self.btn_register)
        self.tabWidget_auth.addTab(tab_register, "Register")
        
        frame_layout.addWidget(self.tabWidget_auth)
        self.btn_back_auth = QtWidgets.QPushButton("← Back to Home")
        self.btn_back_auth.setObjectName("btn_back_auth")
        frame_layout.addWidget(self.btn_back_auth)
        
        layout.addWidget(frame, QtCore.Qt.AlignHCenter)
        self.stackedWidget.addWidget(self.page_auth)

    def setup_page_booking(self):
        """Page 2: Customer booking form."""
        self.page_booking = QtWidgets.QWidget()
        self.page_booking.setObjectName("page_booking")
        layout = QtWidgets.QGridLayout(self.page_booking)
        layout.setSpacing(15)
        
        # Form left
        form_frame = QtWidgets.QFrame()
        form_layout = QtWidgets.QFormLayout(form_frame)
        form_layout.setSpacing(10)
        
        self.input_name = QtWidgets.QLineEdit(placeholderText="Guest name")
        self.input_name.setObjectName("input_name")
        form_layout.addRow("Name:", self.input_name)
        
        self.input_phone = QtWidgets.QLineEdit(placeholderText="Phone")
        self.input_phone.setObjectName("input_phone")
        form_layout.addRow("Phone:", self.input_phone)
        
        self.input_email = QtWidgets.QLineEdit(placeholderText="Email")
        self.input_email.setObjectName("input_email")
        form_layout.addRow("Email:", self.input_email)
        
        self.combo_room_type = QtWidgets.QComboBox()
        self.combo_room_type.addItems(["Select Room", "Standard - $100", "Deluxe - $250", "Suite - $500"])
        self.combo_room_type.setObjectName("combo_room_type")
        form_layout.addRow("Room:", self.combo_room_type)
        
        self.date_checkin = QtWidgets.QDateEdit()
        self.date_checkin.setObjectName("date_checkin")
        self.date_checkin.setCalendarPopup(True)
        form_layout.addRow("Check-in:", self.date_checkin)
        
        self.date_checkout = QtWidgets.QDateEdit()
        self.date_checkout.setObjectName("date_checkout")
        self.date_checkout.setCalendarPopup(True)
        form_layout.addRow("Check-out:", self.date_checkout)
        
        self.spin_guests = QtWidgets.QSpinBox()
        self.spin_guests.setRange(1, 10)
        self.spin_guests.setValue(1)
        self.spin_guests.setObjectName("spin_guests")
        form_layout.addRow("Guests:", self.spin_guests)
        
        self.combo_payment = QtWidgets.QComboBox()
        self.combo_payment.addItems(["Cash at Check-in", "Credit Card", "Transfer"])
        self.combo_payment.setObjectName("combo_payment")
        form_layout.addRow("Payment:", self.combo_payment)
        
        self.txt_requests = QtWidgets.QTextEdit(placeholderText="Special requests...")
        self.txt_requests.setMaximumHeight(80)
        self.txt_requests.setObjectName("txt_requests")
        form_layout.addRow("Requests:", self.txt_requests)
        
        self.btn_confirm = QtWidgets.QPushButton("Confirm Booking")
        self.btn_confirm.setObjectName("btn_confirm")
        self.btn_confirm.setStyleSheet("background: #27ae60; color: white; font-size: 16px; padding: 12px;")
        form_layout.addRow(self.btn_confirm)
        
        layout.addWidget(form_frame, 0, 0)
        
        # Table right
        table_frame = QtWidgets.QFrame()
        table_layout = QtWidgets.QVBoxLayout(table_frame)
        
        self.input_search = QtWidgets.QLineEdit(placeholderText="Search name/ID...")
        self.input_search.setObjectName("input_search")
        table_layout.addWidget(self.input_search)
        
        self.btn_refresh = QtWidgets.QPushButton("🔄 Refresh")
        self.btn_refresh.setObjectName("btn_refresh")
        table_layout.addWidget(self.btn_refresh)
        
        self.table_records = QtWidgets.QTableWidget()
        self.table_records.setColumnCount(8)
        self.table_records.setHorizontalHeaderLabels(["ID", "Name", "Room", "Guests", "Check-in", "Nights", "Status", "Total"])
        self.table_records.setObjectName("table_records")
        table_layout.addWidget(self.table_records)
        
        self.btn_delete = QtWidgets.QPushButton("🗑️ Delete Selected")
        self.btn_delete.setObjectName("btn_delete")
        table_layout.addWidget(self.btn_delete)
        
        self.btn_logout = QtWidgets.QPushButton("Logout")
        self.btn_logout.setObjectName("btn_logout")
        table_layout.addWidget(self.btn_logout)
        
        layout.addWidget(table_frame, 0, 1)
        self.stackedWidget.addWidget(self.page_booking)

    def setup_page_admin(self):
        """Page 3: Admin dashboard (similar to booking + extras)."""
        self.page_admin = QtWidgets.QWidget()
        self.page_admin.setObjectName("page_admin")
        layout = QtWidgets.QVBoxLayout(self.page_admin)
        
        title = QtWidgets.QLabel("👨‍💼 Admin Dashboard")
        title.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("color: #8e44ad; margin: 20px;")
        layout.addWidget(title)
        
        # Reuse similar table/search from booking
        h_layout = QtWidgets.QHBoxLayout()
        self.input_search_admin = QtWidgets.QLineEdit(placeholderText="Admin search...")
        self.input_search_admin.setObjectName("input_search_admin")
        h_layout.addWidget(self.input_search_admin)
        self.btn_refresh_admin = QtWidgets.QPushButton("Refresh All")
        h_layout.addWidget(self.btn_refresh_admin)
        layout.addLayout(h_layout)
        
        self.table_records_admin = QtWidgets.QTableWidget()
        self.table_records_admin.setColumnCount(9)
        self.table_records_admin.setHorizontalHeaderLabels(["ID", "Name", "Phone", "Room", "Guests", "Check-in", "Nights", "Status", "Total"])
        self.table_records_admin.setObjectName("table_records_admin")
        layout.addWidget(self.table_records_admin)
        
        btn_layout = QtWidgets.QHBoxLayout()
        self.btn_delete_admin = QtWidgets.QPushButton("Delete Selected")
        btn_layout.addWidget(self.btn_delete_admin)
        self.btn_logout_admin = QtWidgets.QPushButton("Logout")
        btn_layout.addWidget(self.btn_logout_admin)
        layout.addLayout(btn_layout)
        
        self.stackedWidget.addWidget(self.page_admin)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hotel System v2.0"))
        # Labels already set; additional if needed

