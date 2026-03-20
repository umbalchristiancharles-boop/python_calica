import sys
import os
from typing import Optional, Dict, Any
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, QTableWidgetItem, 
                             QInputDialog, QLineEdit)
from PyQt5.QtCore import Qt
import pymysql
from datetime import date, timedelta
from main_ui_auth import Ui_MainWindow
from auth_handler import AuthHandler

class HotelUI(QMainWindow):
    """Base UI class for Hotel System."""
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

class FrontendApp(HotelUI):
    """Main frontend application for hotel booking system."""
    def __init__(self):
        super().__init__()
        
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'db': 'hotel_db',
            'charset': 'utf8mb4',
            'autocommit': True
        }
        
        self.ui.stackedWidget.setCurrentIndex(0)
        self.logged_in = False
        self.auth_handler = AuthHandler()
        self.current_user: Optional[Dict[str, str]] = None
        
        # Landing page connects - Guest booking removed
        try:
            self.ui.pushButton_auth.clicked.connect(self.show_auth_page)
            print("Auth landing connect OK")
        except AttributeError as e:
            print(f"Landing connect skipped: {e}")
        
        # Other connects with safety
        self._connect_buttons()
        
        # Set default dates if UI available
        try:
            self.ui.date_checkin.setDate(date.today())
            self.ui.date_checkout.setDate(date.today() + timedelta(days=3))
        except AttributeError:
            pass

    def _connect_buttons(self) -> None:
        """Connect all UI buttons safely."""
        connects = [
            (self.ui.btn_confirm.clicked, self.add_booking),
            (self.ui.btn_refresh.clicked, self.refresh_table),
(self.ui.btn_delete.clicked, self.delete_selected),
            (self.ui.input_search.textChanged, self.on_search_changed),
            (self.ui.stackedWidget.currentChanged, self.on_page_changed),
            (self.ui.btn_logout.clicked, self.logout),
            (self.ui.btn_login.clicked, self.handle_login),
            (self.ui.btn_register.clicked, self.handle_register),
            (self.ui.btn_back_auth.clicked, self.show_landing),
        ]
        for signal, slot in connects:
            try:
                signal.connect(slot)
            except AttributeError:
                print(f"Connect skipped: {signal}")

    def get_db_connection(self):
        """Get PyMySQL connection."""
        try:
            conn = pymysql.connect(**self.db_config)
            return conn, conn.cursor(pymysql.cursors.DictCursor)
        except Exception as e:
            QMessageBox.critical(self, "DB Error", f"Connection failed: {e}\\nStart XAMPP MySQL & run hotel_db.sql")
            return None, None

    def load_bookings(self) -> list:
        """Load bookings from DB."""
        conn, cursor = self.get_db_connection()
        if not conn:
            return []
        try:
            search = self.ui.input_search.text() if hasattr(self.ui, 'input_search') else ''
            if search:
                cursor.execute(
                    "SELECT * FROM bookings WHERE name LIKE %s OR id LIKE %s ORDER BY id DESC", 
                    (f"%{search}%", f"%{search}%")
                )
            else:
                cursor.execute("SELECT * FROM bookings ORDER BY id DESC")
            return cursor.fetchall()
        except Exception as e:
            QMessageBox.warning(self, "Load Error", str(e))
            return []
        finally:
            conn.close()

    def populate_customer_info(self):
        """Populate customer info in form."""
        if self.current_user and hasattr(self.ui, 'input_name'):
            self.ui.input_name.setText(self.current_user['name'])
            try:
                self.ui.input_phone.setText(self.current_user['phone'])
                self.ui.input_email.setText(self.current_user['email'])
            except AttributeError:
                pass

    def add_booking(self):
        """Add new booking."""
        if not self.logged_in or self.current_user.get('role') != 'customer':
            return QMessageBox.warning(self, "Access Denied", "Only customers can book")

        try:
            name = self.ui.input_name.text().strip()
            if not name:
                return QMessageBox.warning(self, "Error", "Name required")

            room_type = self.ui.combo_room_type.currentText()
            if "Select" in room_type or "$" not in room_type:
                return QMessageBox.warning(self, "Error", "Select room type")

            checkin = self.ui.date_checkin.date().toPyDate()
            checkout = self.ui.date_checkout.date().toPyDate()
            if checkout <= checkin:
                return QMessageBox.warning(self, "Error", "Valid checkout date required")

            nights = (checkout - checkin).days
            if nights <= 0:
                return QMessageBox.warning(self, "Error", "Minimum 1 night")

            guests = self.ui.spin_guests.value()
            if not (1 <= guests <= 10):
                return QMessageBox.warning(self, "Error", "1-10 guests only")

            # Parse price
            price = 100 if "Standard" in room_type else 250 if "Deluxe" in room_type else 500
            total = price * nights * guests

            conn, cursor = self.get_db_connection()
            if not conn:
                return

            cursor.execute("""
                INSERT INTO bookings (name, phone, email, room_type, checkin, checkout, nights, 
                                    guests, payment, requests, total_bill)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                name,
                getattr(self.ui, 'input_phone', lambda: 'N/A').text(),
                getattr(self.ui, 'input_email', lambda: 'N/A').text(),
                room_type,
                checkin.isoformat(),
                checkout.isoformat(),
                nights,
                guests,
                self.ui.combo_payment.currentText(),
                self.ui.txt_requests.toPlainText(),
                total
            ))
            id_ = cursor.lastrowid
            QMessageBox.information(self, "Success", f"Booked! ID: {id_}\\nTotal: ${total:,.2f}")
            self.clear_form()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            if 'conn' in locals():
                conn.close()

    def clear_form(self):
        """Clear booking form."""
        for field in ['input_name', 'input_phone', 'input_email', 'txt_requests']:
            try:
                getattr(self.ui, field).clear()
            except AttributeError:
                pass
        try:
            self.ui.combo_room_type.setCurrentIndex(0)
            self.ui.combo_payment.setCurrentIndex(0)
            self.ui.spin_guests.setValue(1)
        except AttributeError:
            pass

    def refresh_table(self):
        """Refresh bookings table."""
        bookings = self.load_bookings()
        try:
            table = self.ui.table_records
            table.setRowCount(0)
            for b in bookings:
                row = table.rowCount()
                table.insertRow(row)
                cols = [str(b.get('id', '')), b.get('name', ''), b.get('room_type', ''),
                        str(b.get('guests', '')), str(b.get('checkin', '')), 
                        str(b.get('nights', '')), str(b.get('status', '')), 
                        f"${float(b.get('total_bill', 0)):.2f}"]
                for col, val in enumerate(cols):
                    table.setItem(row, col, QTableWidgetItem(val))
            table.resizeColumnsToContents()
        except AttributeError:
            print("Table UI not available")

    def delete_selected(self):
        """Delete selected booking."""
        try:
            row = self.ui.table_records.currentRow()
            if row < 0:
                return QMessageBox.warning(self, "Error", "Select a row")

            booking_id = self.ui.table_records.item(row, 0).text()
            if QMessageBox.question(self, "Confirm", f"Delete booking ID {booking_id}?") == QMessageBox.No:
                return

            conn, cursor = self.get_db_connection()
            if conn:
                cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
                self.refresh_table()
                QMessageBox.information(self, "Deleted", f"Booking {booking_id} removed")
                conn.close()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

    def on_search_changed(self, text):
        """Handle search change."""
        self.refresh_table()

    def show_auth_page(self):
        """Show auth page."""
        self.ui.stackedWidget.setCurrentIndex(1)

    def show_landing(self):
        """Show landing page."""
        self.ui.stackedWidget.setCurrentIndex(0)

    def handle_login(self):
        """Handle user login."""
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

    def handle_register(self):
        """Handle user registration."""
        try:
            # Get and validate fields
            name = self.ui.input_reg_name.text().strip()
            username = self.ui.input_reg_user.text().strip()
            email = self.ui.input_reg_email.text().strip()
            phone = self.ui.input_reg_phone.text().strip()
            password = self.ui.input_reg_pw.text().strip()
            
            if not all([name, username, email, phone, password]):
                QMessageBox.warning(self, "Validation Error", "All fields are required.")
                return
            
            if len(password) < 6:
                QMessageBox.warning(self, "Validation Error", "Password must be at least 6 characters.")
                self.ui.input_reg_pw.setFocus()
                return
                
            success, msg = self.auth_handler.register(name, username, email, phone, password)
            if success:
                # Clear form and prompt login
                for field in ['input_reg_name', 'input_reg_user', 'input_reg_email', 
                            'input_reg_phone', 'input_reg_pw']:
                    try:
                        getattr(self.ui, field).clear()
                    except AttributeError:
                        pass
                # Switch to login tab if possible
                try:
                    self.ui.tabWidget_auth.setCurrentIndex(0)
                except AttributeError:
                    pass
                QMessageBox.information(self, "Registration Success", 
                    f"Account created for {name}!\nPlease login with your credentials.")
            else:
                QMessageBox.warning(self, "Registration Failed", msg)
        except AttributeError as e:
            print(f"Register UI issue: {e}")
            QMessageBox.critical(self, "UI Error", "Registration interface not loaded.")

    def logout(self):
        """Logout user."""
        self.logged_in = False
        self.current_user = None
        self.show_landing()
        QMessageBox.information(self, "Logged Out", "Thank you!")

    def on_page_changed(self, idx: int):
        """Handle page change security."""
        if idx not in [0, 1, 2, 3]:  # Valid indices
            return
        if not self.logged_in:
            if idx not in [0, 1]:
                self.show_auth_page()
            return
        if self.current_user['role'] == 'admin':
            if idx == 2:
                self.ui.stackedWidget.setCurrentIndex(3)
        else:
            if idx == 3:
                self.ui.stackedWidget.setCurrentIndex(2)
        if idx in [2, 3]:
            self.refresh_table()
            if idx == 2:
                self.populate_customer_info()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = FrontendApp()
    window.show()
    print("Hotel app running. Ensure XAMPP MySQL running & hotel_db.sql executed.")
    sys.exit(app.exec_())

