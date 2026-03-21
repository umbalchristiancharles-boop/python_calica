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
        
        # Place the Login/Register button directly on the landing background
        self.pushButton_auth = QtWidgets.QPushButton("🔐 Login / Register")
        self.pushButton_auth.setObjectName("pushButton_auth")
        self.pushButton_auth.setProperty('class', 'primary')
        self.pushButton_auth.setFont(QtGui.QFont("Segoe UI", 14))
        # Use the primary class defined in main UI stylesheet (Instagram-like gradient)
        self.pushButton_auth.setStyleSheet("QPushButton.primary { min-width: 360px; min-height: 64px; border-radius: 14px; }")
        self.pushButton_auth.setMinimumHeight(64)
        self.pushButton_auth.setMinimumWidth(360)
        self.pushButton_auth.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        self.pushButton_auth.setCursor(QtCore.Qt.PointingHandCursor)
        # Add subtle drop shadow to the landing button for depth
        try:
            shadow_btn = QtWidgets.QGraphicsDropShadowEffect()
            shadow_btn.setBlurRadius(24)
            shadow_btn.setOffset(0, 8)
            shadow_btn.setColor(QtGui.QColor(19, 34, 49, 80))
            self.pushButton_auth.setGraphicsEffect(shadow_btn)
        except Exception:
            pass

        # add spacing to separate title and button, then add button centered
        layout.addSpacing(20)
        layout.addWidget(self.pushButton_auth, alignment=QtCore.Qt.AlignCenter)
        self.stackedWidget.addWidget(self.page_landing)

    def setup_page_auth(self):
        """Page 1: Auth (login/register tabs)."""
        self.page_auth = QtWidgets.QWidget()
        self.page_auth.setObjectName("page_auth")
        layout = QtWidgets.QVBoxLayout(self.page_auth)
        # reduce side margins so content sits closer to center and not too inset
        layout.setContentsMargins(60, 40, 60, 40)
        layout.setSpacing(20)
        # center contents both horizontally and vertically
        try:
            layout.setAlignment(QtCore.Qt.AlignCenter)
        except Exception:
            pass
        
        frame = QtWidgets.QFrame()
        frame.setMaximumWidth(520)
        # Subtle white card used for the auth content, with gentle rounding
        frame.setStyleSheet("""
            background: qlineargradient(to bottom, white, #fbfdff);
            border-radius: 14px; border: none;
            QLineEdit {
                color: #333333;
                padding: 12px;
                border: 1px solid #e3e8ed;
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
        # Add drop shadow to auth card for a floating, modern look
        try:
            card_shadow = QtWidgets.QGraphicsDropShadowEffect()
            card_shadow.setBlurRadius(24)
            card_shadow.setOffset(0, 10)
            card_shadow.setColor(QtGui.QColor(19, 34, 49, 30))
            frame.setGraphicsEffect(card_shadow)
        except Exception:
            pass
        frame_layout = QtWidgets.QVBoxLayout(frame)
        frame_layout.setSpacing(20)
        frame_layout.setContentsMargins(40, 40, 40, 40)
        
        title = QtWidgets.QLabel("Access Your Account")
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
        self.btn_login.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #4facfe, stop:1 #1f6fbf); color: white; font-size: 16px; min-height: 50px; border-radius: 10px; font-weight:700;")
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
        self.btn_register.setStyleSheet("background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #4facfe, stop:1 #1f6fbf); color: white; font-size: 16px; min-height: 50px; border-radius: 10px; font-weight:700;")
        tab_reg_layout.addWidget(self.btn_register)
        self.tabWidget_auth.addTab(tab_register, "Register")
        
        frame_layout.addWidget(self.tabWidget_auth)
        self.btn_back_auth = QtWidgets.QPushButton("← Back to Home")
        self.btn_back_auth.setObjectName("btn_back_auth")
        frame_layout.addWidget(self.btn_back_auth)
        
        # Add stretchers so the frame is vertically centered in the page
        try:
            layout.addStretch(1)
            layout.addWidget(frame, alignment=QtCore.Qt.AlignCenter)
            layout.addStretch(1)
        except Exception:
            layout.addWidget(frame, QtCore.Qt.AlignHCenter)
        self.stackedWidget.addWidget(self.page_auth)

    def setup_page_booking(self):
        """Page 2: Customer booking form."""
        self.page_booking = QtWidgets.QWidget()
        self.page_booking.setObjectName("page_booking")
        layout = QtWidgets.QGridLayout(self.page_booking)
        layout.setSpacing(18)
        
        # Form left
        form_frame = QtWidgets.QFrame()
        form_layout = QtWidgets.QFormLayout(form_frame)
        form_layout.setHorizontalSpacing(24)
        form_layout.setVerticalSpacing(12)
        form_layout.setLabelAlignment(QtCore.Qt.AlignRight)
        
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
        self.btn_confirm.setStyleSheet("background: qlineargradient(spread:pad, x1:0,y1:0,x2:1,y2:0, stop:0 #4facfe, stop:1 #1f6fbf); color: white; font-size: 16px; padding: 12px; border-radius:8px; font-weight:700;")
        form_layout.addRow(self.btn_confirm)

        # Slightly larger fonts for readability in the form
        try:
            font = QtGui.QFont()
            font.setPointSize(10)
            form_frame.setFont(font)
        except Exception:
            pass
        
        layout.addWidget(form_frame, 0, 0)
        
        # Table right
        table_frame = QtWidgets.QFrame()
        table_layout = QtWidgets.QVBoxLayout(table_frame)
        
        self.input_search = QtWidgets.QLineEdit(placeholderText="Search name/ID...")
        self.input_search.setObjectName("input_search")
        table_layout.addWidget(self.input_search)
        
        self.btn_refresh = QtWidgets.QPushButton("🔄 Refresh")
        self.btn_refresh.setObjectName("btn_refresh")
        try:
            self.btn_refresh.setStyleSheet("QPushButton#btn_refresh { background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #4facfe, stop:1 #1f6fbf); color: white; border-radius: 8px; padding: 6px 12px; font-weight:700; }")
            self.btn_refresh.setMinimumHeight(32)
            self.btn_refresh.setCursor(QtCore.Qt.PointingHandCursor)
        except Exception:
            pass
        table_layout.addWidget(self.btn_refresh)
        
        self.table_records = QtWidgets.QTableWidget()
        self.table_records.setColumnCount(8)
        self.table_records.setHorizontalHeaderLabels(["ID", "Name", "Room", "Guests", "Check-in", "Nights", "Status", "Total"])
        self.table_records.setObjectName("table_records")
        # Improve table readability and selection
        try:
            self.table_records.setAlternatingRowColors(True)
            self.table_records.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.table_records.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            # Slightly larger table font
            tbl_font = QtGui.QFont()
            tbl_font.setPointSize(10)
            self.table_records.setFont(tbl_font)
            # Modern visual styles for table and header
            self.table_records.setStyleSheet("""
                QTableWidget { background: #ffffff; border: 1px solid #e6edf3; gridline-color: #f6f9fb; }
                QHeaderView::section { background: #f5f7fa; color: #263238; padding: 6px; font-weight: 700; border-bottom: 1px solid #e6eef6; }
                QTableWidget::item { padding: 6px; color: #26313b; }
                QTableWidget::item:selected { background: #e8f3ff; color: #17202a; }
                QTableWidget::item:hover { background: #f6fbff; }
            """)
            # Header behavior: center labels and use smart resize modes
            header = self.table_records.horizontalHeader()
            header.setDefaultAlignment(QtCore.Qt.AlignCenter)
            try:
                # Explicit per-column resize modes for predictable layout
                header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  # ID
                header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)           # Name
                header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)           # Room
                header.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)  # Guests
                header.setSectionResizeMode(4, QtWidgets.QHeaderView.ResizeToContents)  # Check-in
                header.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)  # Nights
                header.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)  # Status
                header.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)  # Total
            except Exception:
                pass
            # Consistent row height for readability
            self.table_records.verticalHeader().setDefaultSectionSize(28)
        except Exception:
            pass
        table_layout.addWidget(self.table_records)
        
        self.btn_delete = QtWidgets.QPushButton("❌ Cancel Selected")
        self.btn_delete.setObjectName("btn_delete")
        # Make action buttons full-width and consistent
        try:
            self.btn_delete.setMinimumHeight(36)
            self.btn_delete.setStyleSheet("background-color: #e74c3c; color: white; border-radius: 6px;")
        except Exception:
            pass
        table_layout.addWidget(self.btn_delete)
        
        self.btn_rebook = QtWidgets.QPushButton("🔄 Rebook Selected")
        self.btn_rebook.setObjectName("btn_rebook")
        self.btn_rebook.setStyleSheet("""
            QPushButton#btn_rebook {
                background: qlineargradient(spread:pad, x1:0,y1:0,x2:1,y2:0, stop:0 #4facfe, stop:1 #1f6fbf);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 700;
            }
            /* hover brightness removed for compatibility */
        """)
        try:
            self.btn_rebook.setMinimumHeight(36)
        except Exception:
            pass
        table_layout.addWidget(self.btn_rebook)
        
        self.btn_logout = QtWidgets.QPushButton("Logout")
        self.btn_logout.setObjectName("btn_logout")
        try:
            self.btn_logout.setMinimumHeight(30)
            self.btn_logout.setStyleSheet("background-color: #ecf0f1; color: #2c3e50; border-radius: 6px;")
        except Exception:
            pass
        table_layout.addWidget(self.btn_logout)
        
        layout.addWidget(table_frame, 0, 1)
        self.stackedWidget.addWidget(self.page_booking)

    def setup_page_admin(self):
        """Page 3: Admin dashboard (similar to booking + extras)."""
        self.page_admin = QtWidgets.QWidget()
        self.page_admin.setObjectName("page_admin")
        layout = QtWidgets.QVBoxLayout(self.page_admin)
        
        title = QtWidgets.QLabel("Admin Dashboard")
        title.setFont(QtGui.QFont("Segoe UI", 24, QtGui.QFont.Bold))
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("color: #8e44ad; margin: 20px;")
        layout.addWidget(title)
        
        # Reuse similar table/search from booking
        h_layout = QtWidgets.QHBoxLayout()
        self.input_search_admin = QtWidgets.QLineEdit(placeholderText="Admin search...")
        self.input_search_admin.setObjectName("input_search_admin")
        self.input_search_admin.setMinimumHeight(32)
        self.input_search_admin.setStyleSheet("border: 1px solid #d6dce2; border-radius: 8px; padding: 6px 10px; background: white;")
        h_layout.addWidget(self.input_search_admin)
        self.btn_refresh_admin = QtWidgets.QPushButton("Refresh All")
        self.btn_refresh_admin.setObjectName("btn_refresh_admin")
        self.btn_refresh_admin.setMinimumHeight(32)
        self.btn_refresh_admin.setStyleSheet("QPushButton#btn_refresh_admin { background: qlineargradient(x1:0,y1:0,x2:1,y2:0, stop:0 #4facfe, stop:1 #1f6fbf); color: white; border-radius: 8px; padding: 6px 12px; font-weight:700; }")
        h_layout.addWidget(self.btn_refresh_admin)
        layout.addLayout(h_layout)
        
        self.table_records_admin = QtWidgets.QTableWidget()
        self.table_records_admin.setColumnCount(10)
        # Add Username column (index 1) so admin can see which account made the booking
        self.table_records_admin.setHorizontalHeaderLabels(["ID", "Username", "Name", "Phone", "Room", "Guests", "Check-in", "Nights", "Status", "Total"])
        self.table_records_admin.setObjectName("table_records_admin")
        # Improve admin table visuals to match booking table
        try:
            self.table_records_admin.setAlternatingRowColors(True)
            self.table_records_admin.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
            self.table_records_admin.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
            tbl_font = QtGui.QFont()
            tbl_font.setPointSize(10)
            self.table_records_admin.setFont(tbl_font)
            self.table_records_admin.setStyleSheet("""
                QTableWidget { background: #ffffff; border: 1px solid #e6edf3; gridline-color: #f6f9fb; }
                QHeaderView::section { background: #f5f7fa; color: #263238; padding: 6px; font-weight: 700; border-bottom: 1px solid #e6eef6; }
                QTableWidget::item { padding: 6px; color: #26313b; }
                QTableWidget::item:selected { background: #e8f3ff; color: #17202a; }
                QTableWidget::item:hover { background: #f6fbff; }
            """)
            header_adm = self.table_records_admin.horizontalHeader()
            header_adm.setDefaultAlignment(QtCore.Qt.AlignCenter)
            try:
                # Admin table: specify per-column sizing for clarity
                header_adm.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)  # ID
                header_adm.setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeToContents)  # Username
                header_adm.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)           # Name
                header_adm.setSectionResizeMode(3, QtWidgets.QHeaderView.ResizeToContents)  # Phone
                header_adm.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)           # Room
                header_adm.setSectionResizeMode(5, QtWidgets.QHeaderView.ResizeToContents)  # Guests
                header_adm.setSectionResizeMode(6, QtWidgets.QHeaderView.ResizeToContents)  # Check-in
                header_adm.setSectionResizeMode(7, QtWidgets.QHeaderView.ResizeToContents)  # Nights
                header_adm.setSectionResizeMode(8, QtWidgets.QHeaderView.ResizeToContents)  # Status
                header_adm.setSectionResizeMode(9, QtWidgets.QHeaderView.ResizeToContents)  # Total
            except Exception:
                pass
            self.table_records_admin.verticalHeader().setDefaultSectionSize(28)
        except Exception:
            pass
        # Wrap admin table in a light card to improve visual separation
        try:
            table_card = QtWidgets.QFrame()
            table_card.setStyleSheet("background: white; border-radius: 10px; border: 1px solid #e6edf3; padding: 8px;")
            table_layout = QtWidgets.QVBoxLayout(table_card)
            table_layout.setContentsMargins(6,6,6,6)
            table_layout.addWidget(self.table_records_admin)
            layout.addWidget(table_card)
        except Exception:
            layout.addWidget(self.table_records_admin)

        # Add styling for logout button to match admin theming
        try:
            self.btn_logout_admin.setStyleSheet("QPushButton { background: #7f8c8d; color: white; border-radius: 8px; padding: 8px 14px; font-weight:700; } QPushButton:hover { background:#95a5a6; }")
            self.btn_refresh_admin.setCursor(QtCore.Qt.PointingHandCursor)
            self.input_search_admin.setClearButtonEnabled(True)
        except Exception:
            pass
        
        btn_layout = QtWidgets.QHBoxLayout()
        self.btn_delete_admin = QtWidgets.QPushButton("❌ Cancel Selected")
        btn_layout.addWidget(self.btn_delete_admin)
        # Hide admin cancel button per request (keep attribute for backend logic)
        try:
            self.btn_delete_admin.hide()
        except Exception:
            pass

        self.btn_rebook_admin = QtWidgets.QPushButton("🔄 Rebook Selected")
        self.btn_rebook_admin.setObjectName("btn_rebook_admin")
        self.btn_rebook_admin.setStyleSheet("""
            QPushButton#btn_rebook_admin {
                background: qlineargradient(spread:pad, x1:0,y1:0,x2:1,y2:0, stop:0 #4facfe, stop:1 #1f6fbf);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: 700;
            }
            /* hover brightness removed for compatibility */
        """)
        btn_layout.addWidget(self.btn_rebook_admin)
        # Hide admin rebook button per request (keep attribute for backend logic)
        try:
            self.btn_rebook_admin.hide()
        except Exception:
            pass
        
        self.btn_logout_admin = QtWidgets.QPushButton("Logout")
        btn_layout.addWidget(self.btn_logout_admin)
        # UI buttons sized consistently
        layout.addLayout(btn_layout)
        
        self.stackedWidget.addWidget(self.page_admin)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hotel System v2.0"))
        # Labels already set; additional if needed

