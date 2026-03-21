import sys
import os
from typing import Optional, Dict, Any, List
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
        
        # Landing page connects
        try:
            self.ui.pushButton_auth.clicked.connect(self.show_auth_page)
            print("Auth landing connect OK")
        except AttributeError as e:
            print(f"Landing connect skipped: {e}")
        
        # Other connects
        self._connect_buttons()
        
        # Set default dates and connect availability
        try:
            self.ui.date_checkin.setDate(date.today())
            self.ui.date_checkout.setDate(date.today() + timedelta(days=3))
            self.ui.date_checkin.dateChanged.connect(self.on_date_changed)
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
(self.ui.btn_logout_admin.clicked, self.logout),
            (self.ui.input_search_admin.textChanged, self.on_search_changed),
            (self.ui.btn_refresh_admin.clicked, self.refresh_table),
            (self.ui.btn_delete_admin.clicked, self.delete_selected),
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
            QMessageBox.critical(self, "DB Error", f"Connection failed: {e}\nStart XAMPP MySQL & run hotel_db.sql")
            return None, None

    def check_room_availability(self, date_str: str, room_type_id: int) -> bool:
        """Check if room_type_id is available on given date (no overlapping bookings)."""
        conn, cursor = self.get_db_connection()
        if not conn:
            return True  # Offline fallback
        try:
            cursor.execute("""
                SELECT id FROM bookings 
                WHERE room_type_id = %s AND status != 'Cancelled' 
                AND %s >= checkin AND %s < checkout
            """, (room_type_id, date_str, date_str))
            result = cursor.fetchone()
            return result is None
        except Exception as e:
            print(f"Availability check error: {e}")
            return True
        finally:
            conn.close()

    def update_room_availability(self, selected_date: date):
        """Update combo_room_type with available rooms only."""
        try:
            date_str = selected_date.isoformat()
            conn, cursor = self.get_db_connection()
            if not conn:
                return
            
            cursor.execute("SELECT id, name, price_per_night FROM room_types ORDER BY id")
            room_types = cursor.fetchall()
            
            self.ui.combo_room_type.clear()
            self.ui.combo_room_type.addItem("-- Select Available Room --")
            
            for rt in room_types:
                available = self.check_room_availability(date_str, rt['id'])
                display = f"{'✅' if available else '❌'} {rt['name']} - ${rt['price_per_night']}{' (Booked)' if not available else ''}"
                self.ui.combo_room_type.addItem(display)
                index = self.ui.combo_room_type.count() - 1
                self.ui.combo_room_type.model().item(index).setEnabled(available)
            
            conn.close()
        except Exception as e:
            print(f"Update availability error: {e}")
            self.ui.combo_room_type.clear()
            self.ui.combo_room_type.addItems(["Standard - $100", "Deluxe - $250", "Suite - $500"])

    def on_date_changed(self, date_obj):
        """Trigger availability update on date change."""
        try:
            py_date = date_obj.toPyDate()
            self.update_room_availability(py_date)
        except Exception as e:
            print(f"Date change error: {e}")

    def load_bookings(self, user_filter=None) -> list:
        """Load bookings from DB."""
        conn, cursor = self.get_db_connection()
        if not conn:
            return []
        try:
            search = self.ui.input_search.text() if hasattr(self.ui, 'input_search') else ''
            if user_filter and user_filter.get('role') == 'customer':
                name = user_filter.get('name', '')
                email = user_filter.get('email', '')
                phone = user_filter.get('phone', '')
                base_query = "SELECT * FROM bookings WHERE (name = %s OR email = %s OR phone = %s)"
                base_params = (name, email, phone)
                if search:
                    base_query += " AND (name LIKE %s OR id LIKE %s)"
                    base_params += (f"%{search}%", f"%{search}%")
                base_query += " ORDER BY id DESC"
            elif search:
                cursor.execute("SELECT * FROM bookings WHERE name LIKE %s OR id LIKE %s ORDER BY id DESC", (f"%{search}%", f"%{search}%"))
            else:
                try:
                    cursor.execute("SELECT * FROM bookings_view ORDER BY id DESC")
                except:
                    cursor.execute("SELECT b.*, CONCAT(rt.name, ' - $', rt.price_per_night) AS room_type_display FROM bookings b LEFT JOIN room_types rt ON b.room_type_id = rt.id ORDER BY b.id DESC")
                return cursor.fetchall()
            
            cursor.execute(base_query, base_params)
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
        """Add new booking with availability check."""
        if not self.logged_in or self.current_user.get('role') != 'customer':
            return QMessageBox.warning(self, "Access Denied", "Only customers can book")

        try:
            name = self.ui.input_name.text().strip()
            if not name:
                return QMessageBox.warning(self, "Error", "Name required")

            room_type = self.ui.combo_room_type.currentText()
            if "-- Select" in room_type or "$" not in room_type:
                return QMessageBox.warning(self, "Error", "Select available room")

            checkin = self.ui.date_checkin.date().toPyDate()
            checkout = self.ui.date_checkout.date().toPyDate()
            if checkout <= checkin:
                return QMessageBox.warning(self, "Error", "Valid checkout date required")

            room_type_id = 1 if "Standard" in room_type else 2 if "Deluxe" in room_type else 3
            if not self.check_room_availability(checkin.isoformat(), room_type_id):
                return QMessageBox.warning(self, "Room Unavailable", f"Room type booked on {checkin}. Choose another.")

            nights = (checkout - checkin).days
            guests = self.ui.spin_guests.value()
            price = 100 if "Standard" in room_type else 250 if "Deluxe" in room_type else 500
            total = price * nights * guests

            conn, cursor = self.get_db_connection()
            if not conn:
                return

            user_id = self.current_user.get('id') if self.current_user and 'id' in self.current_user else None
            cursor.execute("""
                INSERT INTO bookings (user_id, room_type_id, name, phone, email, checkin, checkout, nights, 
                                      guests, payment, requests, total_bill)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (user_id, room_type_id, name, self.ui.input_phone.text(), self.ui.input_email.text(), 
                  checkin.isoformat(), checkout.isoformat(), nights, guests, self.ui.combo_payment.currentText(),
                  self.ui.txt_requests.toPlainText(), total))
            
            id_ = cursor.lastrowid
            QMessageBox.information(self, "Success", f"Booked! ID: {id_}\nTotal: ${total:,.2f}")
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
        """Refresh bookings table - page aware."""
        user_filter = self.current_user if self.logged_in and self.current_user.get('role') == 'customer' else None
        current_page = self.ui.stackedWidget.currentIndex()
        is_admin = current_page == 3
        table = self.ui.table_records_admin if is_admin else self.ui.table_records
        search_field = self.ui.input_search_admin if is_admin else self.ui.input_search
        bookings = self.load_bookings(user_filter)
        table.setRowCount(0)
        for b in bookings:
            row = table.rowCount()
            table.insertRow(row)
            cols = [str(b.get('id', ''))]
            cols.append(b.get('name', ''))
            if is_admin:
                cols.append(b.get('phone', ''))
            cols += [b.get('room_type_display', b.get('room_type', '')),
                     str(b.get('guests', '')), str(b.get('checkin', '')),
                     str(b.get('nights', '')), b.get('status', ''),
                     f"${float(b.get('total_bill', 0)):.2f}"]
            for col, val in enumerate(cols):
                table.setItem(row, col, QTableWidgetItem(str(val)))
            table.resizeColumnsToContents()

    # Placeholder for missing methods - expand with original full implementations
    def delete_selected(self):
        """Delete selected booking from DB."""
        current_page = self.ui.stackedWidget.currentIndex()
        is_admin = current_page == 3
        table = self.ui.table_records_admin if is_admin else self.ui.table_records
        selection = table.selectedItems()
        if not selection:
            return QMessageBox.warning(self, "No Selection", "Select a booking row first.")
        
        row = selection[0].row()
        booking_id = int(table.item(row, 0).text())
        reply = QMessageBox.question(self, 'Confirm Delete', f'Delete booking ID {booking_id}?',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            conn, cursor = self.get_db_connection()
            if conn:
                try:
                    cursor.execute("DELETE FROM bookings WHERE id = %s", (booking_id,))
                    table.removeRow(row)
                    self.refresh_table()
                    QMessageBox.information(self, "Deleted", f"Booking {booking_id} deleted.")
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Delete failed: {e}")
                finally:
                    conn.close()
            else:
                QMessageBox.warning(self, "DB Error", "Cannot connect to database.")

    def on_search_changed(self, text):
        """Search change - page aware."""
        self.refresh_table()

    def show_auth_page(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def show_landing(self):
        self.ui.stackedWidget.setCurrentIndex(0)

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
                self._sync_user_to_db(user)
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
                "INSERT INTO users (name, username, email, phone, password, role) VALUES (%s,%s,%s,%s,%s,%s)",
                (user.get('name'), user.get('username'), user.get('email'), user.get('phone'), user.get('password'), user.get('role', 'customer'))
            )
            cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
            row = cursor.fetchone()
            if row and row.get('id'):
                user['id'] = row.get('id')
            conn.close()
        except Exception:
            pass  # Non-fatal

    def handle_register(self):
        '''Handle user registration.'''
        try:
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
                new_user = self.auth_handler.login(username, password)
                if new_user:
                    self._sync_user_to_db(new_user)

                for field in ['input_reg_name', 'input_reg_user', 'input_reg_email', 
                              'input_reg_phone', 'input_reg_pw']:
                    try:
                        getattr(self.ui, field).clear()
                    except AttributeError:
                        pass
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
        reply = QMessageBox.question(self, 'Confirm Logout', 'Are you sure you want to logout?', 
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.logged_in = False
            self.current_user = None
            self.show_landing()

    def on_page_changed(self, idx: int):
        """Page change security."""
        pass  # Full impl in original

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = FrontendApp()
    window.show()
    print("Hotel app running. Ensure XAMPP MySQL running & hotel_db.sql executed.")
    sys.exit(app.exec_())

