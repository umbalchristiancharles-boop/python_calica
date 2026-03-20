import sys
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, QTableWidgetItem)
from PyQt5.QtCore import Qt
import pymysql
from datetime import date, timedelta
from main_ui import Ui_MainWindow

class HotelUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

class FrontendApp(HotelUI):
    def __init__(self):
        super().__init__()
        
        # for db ito
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': '',
            'db': 'hotel_db',
            'charset': 'utf8mb4',
            'autocommit': True
        }
        
        # Landing page ito
        self.ui.stackedWidget.setCurrentIndex(0)
        self.logged_in = False
        
        # Navigation
        try:
            self.ui.pushButton.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_booking))
            self.ui.pushButton_2.clicked.connect(self.admin_login)
            self.ui.btn_back.clicked.connect(lambda: self.ui.stackedWidget.setCurrentWidget(self.ui.page_landing))
            print("Navigation connected.")
        except:
            print("Navigation setup skipped.")
        
        # function ng booking
        try:
            self.ui.btn_confirm.clicked.connect(self.add_booking)
            self.ui.btn_refresh.clicked.connect(self.refresh_table)
            self.ui.btn_delete.clicked.connect(self.delete_selected)
            self.ui.input_search.textChanged.connect(self.on_search_changed)
            self.ui.stackedWidget.currentChanged.connect(self.on_page_changed)
            self.ui.btn_logout.clicked.connect(self.logout)
            # default dates 
            self.ui.date_checkin.setDate(date.today())
            self.ui.date_checkout.setDate(date.today() + timedelta(days=3))
            print("Booking module connected.")
        except:
            print("Booking setup skipped.")

    def get_db_connection(self):
        try:
            conn = pymysql.connect(**self.db_config)
            return conn, conn.cursor(pymysql.cursors.DictCursor)
        except Exception as e:
            QMessageBox.critical(self, "DB Error", f"Connection failed: {e}\nStart XAMPP MySQL & run create_hotel_db.sql")
            return None, None

    def load_bookings(self):
        conn, cursor = self.get_db_connection()
        if not conn:
            return []
        try:
            search = self.ui.input_search.text()
            if search:
                cursor.execute("SELECT * FROM bookings WHERE name LIKE %s OR id LIKE %s ORDER BY id DESC", (f"%{search}%", f"%{search}%"))
            else:
                cursor.execute("SELECT * FROM bookings ORDER BY id DESC")
            return cursor.fetchall()
        except Exception as e:
            QMessageBox.warning(self, "Load Error", str(e))
            return []
        finally:
            conn.close()

    def add_booking(self):
        name = self.ui.input_name.text().strip()
        if not name:
            return QMessageBox.warning(self, "Error", "Name required")
        
        room_type = self.ui.combo_room_type.currentText()
        if "Select" in room_type or "$" not in room_type:
            return QMessageBox.warning(self, "Error", "Room type required")
        
        checkin = self.ui.date_checkin.date().toPyDate()
        checkout = self.ui.date_checkout.date().toPyDate()
        if checkout <= checkin:
            return QMessageBox.warning(self, "Error", "Valid dates required")
        
        nights = (checkout - checkin).days
        if nights <= 0:
            return QMessageBox.warning(self, "Error", "Minimum 1 night")
        
        guests = self.ui.spin_guests.value()
        if not (1 <= guests <= 10):
            return QMessageBox.warning(self, "Error", "1-10 guests")
        
        # Price from room_type
        if "Standard" in room_type:
            price = 100
        elif "Deluxe" in room_type:
            price = 250
        else:
            price = 500
        total = price * nights * guests
        
        conn, cursor = self.get_db_connection()
        if not conn:
            return
        
        try:
            cursor.execute("""
                INSERT INTO bookings (name, phone, email, room_type, checkin, checkout, nights, guests, payment, requests, total_bill)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                name,
                self.ui.input_phone.text(),
                self.ui.input_email.text(),
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
            QMessageBox.information(self, "Success", f"Booked! ID: {id_}\nTotal: ${total}")
            self.clear_form()
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
        finally:
            conn.close()

    def clear_form(self):
        self.ui.input_name.clear()
        self.ui.input_phone.clear()
        self.ui.input_email.clear()
        self.ui.txt_requests.clear()
        self.ui.combo_room_type.setCurrentIndex(0)
        self.ui.combo_payment.setCurrentIndex(0)
        self.ui.spin_guests.setValue(1)

    def refresh_table(self):
        bookings = self.load_bookings()
        table = self.ui.table_records
        table.setRowCount(0)
        for b in bookings:
            row = table.rowCount()
            table.insertRow(row)
            table.setItem(row, 0, QTableWidgetItem(str(b['id'])))
            table.setItem(row, 1, QTableWidgetItem(b['name']))
            table.setItem(row, 2, QTableWidgetItem(b['room_type']))
            table.setItem(row, 3, QTableWidgetItem(str(b['guests'])))
            table.setItem(row, 4, QTableWidgetItem(str(b['checkin'])))
            table.setItem(row, 5, QTableWidgetItem(str(b['nights'])))
            table.setItem(row, 6, QTableWidgetItem(str(b['status'])))
            table.setItem(row, 7, QTableWidgetItem(f"${b['total_bill']:.2f}"))
        table.resizeColumnsToContents()

    def delete_selected(self):
        row = self.ui.table_records.currentRow()
        if row < 0:
            return QMessageBox.warning(self, "Error", "Select row")
        
        booking_id = self.ui.table_records.item(row, 0).text()
        if QMessageBox.question(self, "Confirm", f"Delete ID {booking_id}?") == QMessageBox.No:
            return
        
        conn, cursor = self.get_db_connection()
        if conn:
            try:
                cursor.execute("DELETE FROM bookings WHERE id=%s", (booking_id,))
                self.refresh_table()
                QMessageBox.information(self, "Deleted", "Done")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))
            conn.close()

    def on_search_changed(self, text):
        self.refresh_table()

    def on_page_changed(self, idx):
        if idx == 2:  # Admin
            if not self.logged_in:
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_landing)
                QMessageBox.warning(self, "Access Denied", "Please login first.")
                return
            self.refresh_table()
        elif idx == 0:
            self.logged_in = False

    def admin_login(self):
        from PyQt5.QtWidgets import QInputDialog, QLineEdit
        username, ok1 = QInputDialog.getText(self, "Admin Login", "Username:", QLineEdit.Normal, "")
        if not ok1 or not username:
            return
        
        password, ok2 = QInputDialog.getText(self, "Admin Login", "Password:", QLineEdit.Password, "")
        if not ok2 or not password:
            return
        
        conn, cursor = self.get_db_connection()
        if not conn:
            return
        
        try:
            cursor.execute("SELECT * FROM admins WHERE username = %s AND password = %s", (username, password))
            admin = cursor.fetchone()
            if admin:
                self.logged_in = True
                self.ui.stackedWidget.setCurrentWidget(self.ui.page_admin)
                self.refresh_table()
                QMessageBox.information(self, "Success", f"Welcome, {username}!")
            else:
                QMessageBox.warning(self, "Login Failed", "Invalid credentials.")
        except Exception as e:
            QMessageBox.critical(self, "DB Error", str(e))
        finally:
            conn.close()

    def logout(self):
        self.logged_in = False
        self.ui.stackedWidget.setCurrentWidget(self.ui.page_landing)
        QMessageBox.information(self, "Logged Out", "Goodbye!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = FrontendApp()
    window.show()
    print("Hotel app running. Run create_hotel_db.sql first!")
    sys.exit(app.exec_())
