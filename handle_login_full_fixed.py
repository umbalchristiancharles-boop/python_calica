from PyQt5.QtWidgets import QMessageBox
from typing import Dict

def handle_login(self):
    '''Handle user login.'''
    try:
        username = self.ui.input_login_user.text().strip()
        password = self.ui.input_login_pw.text().strip()
        if not username or not password:
            self.ui.input_login_user.clear()
            self.ui.input_login_pw.clear()
            self.ui.input_login_user.setFocus()
            return QMessageBox.warning(self, "Error", "Please enter both username and password.")

        user = self.auth_handler.login(username, password)
        if user:
            # Sync to DB and attach ID
            _sync_user_to_db(self, user)
            self.current_user = user
            self.logged_in = True
            self.ui.input_login_user.clear()
            self.ui.input_login_pw.clear()
            if user['role'] == 'admin':
                self.ui.stackedWidget.setCurrentIndex(3)
                self.refresh_table()
            else:
                self.ui.stackedWidget.setCurrentIndex(2)
                self.populate_customer_info()
            QMessageBox.information(self, "Welcome", f"Hi, {user['name']}! ({user['role'].title()})")
        else:
            self.ui.input_login_user.clear()
            self.ui.input_login_pw.clear()
            self.ui.input_login_user.setFocus()
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")
    except AttributeError as e:
        print(f"Login UI issue: {e}")
        QMessageBox.critical(self, "UI Error", "Login interface not loaded properly.")

def _sync_user_to_db(self, user: Dict) -> None:
    '''Sync user to DB and attach ID.'''
    try:
        conn, cursor = self.get_db_connection()
        if not conn:
            return

        username = user.get('username')
        email = user.get('email')

        cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
        row = cursor.fetchone()
        if row and row.get('id'):
            user['id'] = row.get('id')
            conn.close()
            return

        cursor.execute(
            "INSERT INTO users (name, username, email, phone, password, role) VALUES (%s, %s, %s, %s, %s, %s)",
            (user.get('name'), user.get('username'), user.get('email'), user.get('phone'), user.get('password'), user.get('role', 'customer'))
        )
        cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
        row = cursor.fetchone()
        if row and row.get('id'):
            user['id'] = row.get('id')
        conn.close()
    except Exception:
        pass  # Non-fatal

# Usage: Copy these methods into FrontendApp class in main_frontend_fixed.py

