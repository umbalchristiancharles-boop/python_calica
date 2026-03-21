import sys
import os
from typing import Optional, Dict, Any, List
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMessageBox, QTableWidgetItem, 
                             QInputDialog, QLineEdit)
from PyQt5 import QtGui, QtWidgets, QtCore
from PyQt5.QtCore import Qt, QTimer
import pymysql
from datetime import date, timedelta
import datetime
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
        # Enhance landing button interactivity and appearance at runtime
        try:
            btn = getattr(self.ui, 'pushButton_auth', None)
            if btn:
                try:
                    from PyQt5 import QtGui, QtWidgets, QtCore
                    btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
                    btn.setStyleSheet(btn.styleSheet() + "\nQPushButton#pushButton_auth { padding: 16px 36px; font-size: 16px; font-weight: 600; }")
                    try:
                        shadow = QtWidgets.QGraphicsDropShadowEffect(self)
                        shadow.setBlurRadius(18)
                        shadow.setOffset(0, 6)
                        shadow.setColor(QtGui.QColor(0, 0, 0, 80))
                        btn.setGraphicsEffect(shadow)
                    except Exception:
                        pass
                except Exception:
                    pass
        except Exception:
            pass
        
        # Other connects
        self._connect_buttons()
        
        # Set default dates and connect availability
        try:
            self.ui.date_checkin.setDate(date.today())
            self.ui.date_checkout.setDate(date.today() + timedelta(days=3))
            self.ui.date_checkin.dateChanged.connect(self.on_date_changed)
        except AttributeError:
            pass

        # Auto-refresh timer: refresh bookings table periodically when relevant page is active
        try:
            self.auto_refresh_timer = QTimer(self)
            self.auto_refresh_timer.setInterval(5000)  # 5 seconds
            self.auto_refresh_timer.timeout.connect(self._auto_refresh_tick)
            self.auto_refresh_timer.start()
        except Exception:
            pass

        # Ensure DB schema has expected columns (self-healing migration)
        try:
            self.ensure_booking_columns()
        except Exception as e:
            print(f"Schema migration check failed: {e}")

        # Guard to avoid overlapping refreshes that freeze the UI
        self._refresh_in_progress = False

    def _connect_buttons(self) -> None:
        """Connect all UI buttons safely."""
        connects = [
            (self.ui.btn_confirm.clicked, self.add_booking),
            (self.ui.btn_refresh.clicked, self.refresh_table),
            (self.ui.btn_delete.clicked, self.cancel_selected_booking),
            (self.ui.input_search.textChanged, self.on_search_changed),
            (self.ui.stackedWidget.currentChanged, self.on_page_changed),
            (self.ui.btn_logout.clicked, self.logout),
            (self.ui.btn_logout_admin.clicked, self.logout),
            (self.ui.input_search_admin.textChanged, self.on_search_changed),
            (self.ui.btn_refresh_admin.clicked, self.refresh_table),
            (self.ui.btn_delete_admin.clicked, self.delete_user_prompt),
            (self.ui.btn_rebook.clicked, self.rebook_selected),
            (self.ui.btn_rebook_admin.clicked, self.rebook_selected),
            (self.ui.btn_login.clicked, self.handle_login),
            (self.ui.btn_register.clicked, self.handle_register),
            (self.ui.btn_back_auth.clicked, self.show_landing),
        ]

        for signal, slot in connects:
            try:
                signal.connect(slot)
            except AttributeError:
                print(f"Connect skipped: {signal}")
        # No approve button to connect (removed from UI)
        # Connect selection change to update action buttons when tables exist
        try:
            self.ui.table_records.itemSelectionChanged.connect(self.update_action_buttons)
        except Exception:
            pass
        try:
            self.ui.table_records_admin.itemSelectionChanged.connect(self.update_action_buttons)
        except Exception:
            pass
        # Double click shows booking details (customer panel)
        try:
            self.ui.table_records.itemDoubleClicked.connect(self.show_booking_details)
        except Exception:
            pass
        # No client-side approve button; admin approvals handled server-side

    def get_db_connection(self):
        """Get PyMySQL connection."""
        try:
            conn = pymysql.connect(**self.db_config)
            return conn, conn.cursor(pymysql.cursors.DictCursor)
        except Exception as e:
            QMessageBox.critical(self, "DB Error", f"Connection failed: {e}\nStart XAMPP MySQL & run hotel_db.sql")
            return None, None

    def ensure_booking_columns(self):
        """Ensure `rebooked_from_id` and `rebooking_reason` columns exist on `bookings` table; add if missing."""
        conn, cursor = self.get_db_connection()
        if not conn:
            return
        try:
            # Check and add rebooked_from_id
            cursor.execute("""
                SELECT COUNT(*) AS cnt FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'bookings' AND COLUMN_NAME = 'rebooked_from_id'
            """, (self.db_config.get('db'),))
            row = cursor.fetchone()
            if row and row.get('cnt', 0) == 0:
                try:
                    cursor.execute("ALTER TABLE bookings ADD COLUMN rebooked_from_id INT NULL")
                except Exception:
                    pass
                try:
                    cursor.execute("ALTER TABLE bookings ADD CONSTRAINT fk_rebooked_from FOREIGN KEY (rebooked_from_id) REFERENCES bookings(id) ON DELETE SET NULL")
                except Exception:
                    pass
                print("Added missing column rebooked_from_id to bookings table.")

            # Check and add rebooking_reason
            cursor.execute("""
                SELECT COUNT(*) AS cnt FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_SCHEMA = %s AND TABLE_NAME = 'bookings' AND COLUMN_NAME = 'rebooking_reason'
            """, (self.db_config.get('db'),))
            row2 = cursor.fetchone()
            if row2 and row2.get('cnt', 0) == 0:
                try:
                    cursor.execute("ALTER TABLE bookings ADD COLUMN rebooking_reason TEXT NULL")
                    print("Added missing column rebooking_reason to bookings table.")
                except Exception:
                    pass
        finally:
            conn.close()

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
                display = f"{ '✅' if available else '❌' } {rt['name']} - ${rt['price_per_night']}{' (Booked)' if not available else ''}"
                self.ui.combo_room_type.addItem(display)
                index = self.ui.combo_room_type.count() - 1
                try:
                    self.ui.combo_room_type.model().item(index).setEnabled(available)
                except Exception:
                    pass
            
            conn.close()
        except Exception as e:
            print(f"Update availability error: {e}")
            try:
                self.ui.combo_room_type.clear()
                self.ui.combo_room_type.addItems(["Standard - $100", "Deluxe - $250", "Suite - $500"])
            except Exception:
                pass

    def on_date_changed(self, date_obj):
        """Trigger availability update on date change."""
        try:
            py_date = date_obj.toPyDate()
            self.update_room_availability(py_date)
        except Exception as e:
            print(f"Date change error: {e}")

    def _auto_refresh_tick(self):
        """Called by QTimer periodically; refresh table only when booking/admin pages are visible."""
        try:
            current_page = self.ui.stackedWidget.currentIndex()
            # customer page is 2, admin is 3
            if current_page in (2, 3):
                self.refresh_table()
        except Exception:
            pass

    def load_bookings(self, user_filter=None) -> list:
        """Load bookings from DB."""
        conn, cursor = self.get_db_connection()
        if not conn:
            return []
        try:
            search = self.ui.input_search.text() if hasattr(self.ui, 'input_search') else ''
            if user_filter and user_filter.get('role') == 'customer':
                # Filter bookings by the user's DB id to avoid exposing others' data
                user_id = user_filter.get('id')
                base_query = "SELECT * FROM bookings WHERE user_id = %s"
                base_params = (user_id,)
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
            # Handle rebook
            if hasattr(self, 'pending_rebook'):
                # Backend ownership check for rebook: ensure current user owns original booking (unless admin)
                try:
                    conn_check, cursor_check = self.get_db_connection()
                    if conn_check:
                        cursor_check.execute("SELECT user_id FROM bookings WHERE id = %s", (self.pending_rebook['from_id'],))
                        orig = cursor_check.fetchone()
                        orig_owner = orig.get('user_id') if orig else None
                        conn_check.close()
                        if not (self.logged_in and (self.current_user and self.current_user.get('role') == 'admin' or orig_owner == (self.current_user.get('id') if self.current_user else None))):
                            return QMessageBox.warning(self, "Access Denied", "You are not allowed to rebook this reservation")
                except Exception:
                    # If ownership check cannot be completed, block for safety
                    return QMessageBox.warning(self, "Access Denied", "Unable to validate rebook ownership")

                cursor.execute("""
                    INSERT INTO bookings (user_id, room_type_id, name, phone, email, checkin, checkout, nights, 
                                          guests, payment, requests, total_bill, rebooked_from_id, rebooking_reason)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, room_type_id, name, self.ui.input_phone.text(), self.ui.input_email.text(), 
                      checkin.isoformat(), checkout.isoformat(), nights, guests, self.ui.combo_payment.currentText(),
                      self.ui.txt_requests.toPlainText(), total, self.pending_rebook['from_id'], self.pending_rebook['reason']))
                del self.pending_rebook
                msg = "Rebooked successfully! (linked to original)"
            else:
                cursor.execute("""
                    INSERT INTO bookings (user_id, room_type_id, name, phone, email, checkin, checkout, nights, 
                                          guests, payment, requests, total_bill)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (user_id, room_type_id, name, self.ui.input_phone.text(), self.ui.input_email.text(), 
                      checkin.isoformat(), checkout.isoformat(), nights, guests, self.ui.combo_payment.currentText(),
                      self.ui.txt_requests.toPlainText(), total))
                msg = f"Booked! ID: {cursor.lastrowid}\\nTotal: ${total:,.2f}"
            
            id_ = cursor.lastrowid
            QMessageBox.information(self, "Success", msg)
            
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
        # Avoid overlapping refreshes
        if getattr(self, '_refresh_in_progress', False):
            return
        self._refresh_in_progress = True
        try:
            user_filter = self.current_user if self.logged_in and self.current_user.get('role') == 'customer' else None
            current_page = self.ui.stackedWidget.currentIndex()
            is_admin = current_page == 3
            # If admin view, reload users from disk so manual edits reflect immediately
            if is_admin:
                try:
                    self.auth_handler.users = self.auth_handler.load_users()
                except Exception:
                    pass
            table = self.ui.table_records_admin if is_admin else self.ui.table_records
            search_field = self.ui.input_search_admin if is_admin else self.ui.input_search
            bookings = self.load_bookings(user_filter)
            table.setRowCount(0)

            for b in bookings:
                row = table.rowCount()
                table.insertRow(row)
                # For admin view include username as second column
                if is_admin:
                    cols = [str(b.get('id', '')), b.get('username', ''), b.get('name', ''), b.get('phone', '')]
                else:
                    cols = [str(b.get('id', '')), b.get('name', '')]

                status = b.get('status', '') or ''
                status_display = status
                try:
                    if status == 'Cancelled' and b.get('cancellation_reason'):
                        status_display = f"{status}\\n({b.get('cancellation_reason','')[:30]}...)"
                except Exception:
                    status_display = status

                try:
                    if is_admin and status == 'Cancellation Requested':
                        user_tag = b.get('username') or b.get('user_name') or ''
                        user_part = f" by {user_tag}" if user_tag else ''
                        status_display = f"Cancellation Requested{user_part}\\n({b.get('cancellation_reason','')[:40]}...)"
                except Exception:
                    pass

                cols += [b.get('room_type_display', b.get('room_type', '')),
                         str(b.get('guests', '')), str(b.get('checkin', '')),
                         str(b.get('nights', '')), 
                         status_display,
                         f"${float(b.get('total_bill', 0)):.2f}"]
                for col, val in enumerate(cols):
                    table.setItem(row, col, QTableWidgetItem(str(val)))

                # Color the Status cell as a small badge (background color)
                try:
                    status_text = (b.get('status') or '').strip()
                    # Status column index depends on whether username column is present (admin view)
                    status_idx = 8 if is_admin else 6
                    status_item = table.item(row, status_idx)
                    if status_item:
                        st = status_text.lower()
                        if st.startswith('cancel'):
                            status_item.setBackground(QtGui.QColor('#f1948a'))
                        elif st.startswith('cancellation requested'):
                            status_item.setBackground(QtGui.QColor('#f7dc6f'))
                        elif st.startswith('confirmed'):
                            status_item.setBackground(QtGui.QColor('#abebc6'))
                        else:
                            status_item.setBackground(QtGui.QColor('#d5dbdb'))
                except Exception:
                    pass

            try:
                table.resizeColumnsToContents()
            except Exception:
                pass
        finally:
            self._refresh_in_progress = False

    # Placeholder for missing methods - expand with original full implementations
    def cancel_selected_booking(self):
        """Cancel selected booking (mark as Cancelled + reason)."""
        current_page = self.ui.stackedWidget.currentIndex()
        is_admin = current_page == 3
        table = self.ui.table_records_admin if is_admin else self.ui.table_records
        selection = table.selectedItems()
        if not selection:
            return QMessageBox.warning(self, "No Selection", "Select a booking row first.")
        
        row = selection[0].row()
        booking_id = int(table.item(row, 0).text())
        # Safety: check current status to prevent duplicate cancels
        conn_check, cursor_check = self.get_db_connection()
        if not conn_check:
            return QMessageBox.warning(self, "DB Error", "Cannot connect to database.")
        try:
            cursor_check.execute("SELECT status FROM bookings WHERE id = %s", (booking_id,))
            row_check = cursor_check.fetchone()
            current_status = row_check.get('status') if row_check else None
        finally:
            conn_check.close()

        if current_status in ('Cancelled', 'Cancellation Requested', 'Cancellation Approved'):
            return QMessageBox.warning(self, "Already Processed", f"Booking {booking_id} has status '{current_status}' and cannot be cancelled again.")

        reply = QMessageBox.question(self, 'Confirm Cancel', f'Cancel booking ID {booking_id}?\nThis will mark it as Cancelled.',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            reason, ok = QInputDialog.getText(self, 'Cancellation Reason', 'Enter reason (required):', text='')
            if ok and reason.strip():
                conn, cursor = self.get_db_connection()
                if conn:
                    try:
                        # Security check: verify ownership on the backend before updating
                        cursor.execute("SELECT user_id FROM bookings WHERE id = %s", (booking_id,))
                        row = cursor.fetchone()
                        owner_id = row.get('user_id') if row else None
                        if not is_admin:
                            if not self.logged_in or self.current_user is None or owner_id != self.current_user.get('id'):
                                return QMessageBox.warning(self, "Access Denied", "You are not allowed to modify this booking")

                        if not is_admin:
                            # For customers: create a cancellation request instead of immediate cancel
                            try:
                                cursor.execute("UPDATE bookings SET status = 'Cancellation Requested', cancellation_reason = %s WHERE id = %s", (reason, booking_id))
                            except pymysql.err.InternalError as ie:
                                if ie.args and ie.args[0] == 1054:
                                    cursor.execute("UPDATE bookings SET status = 'Cancellation Requested' WHERE id = %s", (booking_id,))
                                else:
                                    raise
                            self.refresh_table()
                            QMessageBox.information(self, "Requested", f"Cancellation requested for booking {booking_id}. Awaiting admin approval.")
                        else:
                            # Admin can cancel immediately
                            try:
                                cursor.execute("UPDATE bookings SET status = 'Cancelled', cancellation_reason = %s WHERE id = %s", (reason, booking_id))
                            except pymysql.err.InternalError as ie:
                                if ie.args and ie.args[0] == 1054:
                                    cursor.execute("UPDATE bookings SET status = 'Cancelled' WHERE id = %s", (booking_id,))
                                else:
                                    raise
                            self.refresh_table()
                            QMessageBox.information(self, "Cancelled", f"Booking {booking_id} cancelled.\nReason: {reason[:50]}...")
                    except Exception as e:
                        QMessageBox.critical(self, "Error", f"Cancel failed: {e}")
                    finally:
                        conn.close()
                else:
                    QMessageBox.warning(self, "DB Error", "Cannot connect to database.")
            else:
                return QMessageBox.warning(self, "Cancelled", "No reason provided.")

    def delete_user_prompt(self):
        """Prompt admin to delete a user from local users.json and (if present) remove from DB."""
        if not self.logged_in or not self.current_user or self.current_user.get('role') != 'admin':
            return QMessageBox.warning(self, "Access Denied", "Only admin can delete users.")

        username, ok = QtWidgets.QInputDialog.getText(self, 'Delete User', 'Enter username to delete:')
        if not ok or not username.strip():
            return

        username = username.strip()
        reply = QMessageBox.question(self, 'Confirm Delete', f"Delete user '{username}'? This cannot be undone.", QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        success, msg = self.auth_handler.delete_user(username)
        if success:
            # Optionally remove from DB as well
            try:
                conn, cursor = self.get_db_connection()
                if conn:
                    try:
                        cursor.execute("DELETE FROM users WHERE username = %s OR email = %s", (username, username))
                    except Exception:
                        pass
                    conn.close()
            except Exception:
                pass
            # Reload local users and refresh admin table so UI updates immediately
            try:
                self.auth_handler.users = self.auth_handler.load_users()
            except Exception:
                pass
            try:
                self.refresh_table()
            except Exception:
                pass
            QMessageBox.information(self, 'Deleted', msg)
        else:
            QMessageBox.warning(self, 'Delete Failed', msg)

    def update_action_buttons(self):
        """Enable/disable booking action buttons based on ownership and selection."""
        try:
            current_page = self.ui.stackedWidget.currentIndex()
            is_admin = current_page == 3
            table = self.ui.table_records_admin if is_admin else self.ui.table_records
            selected = table.selectedItems()
            # Default disable
            for btn in [getattr(self.ui, 'btn_delete', None), getattr(self.ui, 'btn_rebook', None)]:
                try:
                    if btn:
                        btn.setEnabled(False)
                except Exception:
                    pass

            if not selected:
                return

            row = selected[0].row()
            try:
                booking_id = int(table.item(row, 0).text())
            except Exception:
                return

            conn, cursor = self.get_db_connection()
            if not conn:
                return
            try:
                cursor.execute("SELECT user_id, status FROM bookings WHERE id = %s", (booking_id,))
                db_row = cursor.fetchone()
                owner_id = db_row.get('user_id') if db_row else None
                status = db_row.get('status') if db_row else None
                print(f"update_action_buttons: booking_id={booking_id} db_row_exists={bool(db_row)} status={status}")
            finally:
                conn.close()

            # Admin view: enable approve button only when a cancellation request is selected
            if is_admin:
                try:
                    # Default disable admin action buttons
                    if getattr(self.ui, 'btn_delete_admin', None):
                        self.ui.btn_delete_admin.setEnabled(False)
                    if getattr(self.ui, 'btn_rebook_admin', None):
                        self.ui.btn_rebook_admin.setEnabled(False)
                except Exception:
                    pass
                return

            # For customer view: enable only if logged in and owner
            is_owner = self.logged_in and self.current_user and owner_id == self.current_user.get('id')
            # Do not allow cancelling/re-requesting if already processed or pending
            # 'Confirmed' should be cancellable by customers (it means active booking)
            processed_statuses = ['Cancelled', 'Cancellation Approved', 'Checked-in', 'Checked-out']
            is_pending = status == 'Cancellation Requested'
            can_cancel = is_owner and (status not in processed_statuses) and (not is_pending)
            try:
                if getattr(self.ui, 'btn_delete', None):
                    self.ui.btn_delete.setEnabled(can_cancel)
                if getattr(self.ui, 'btn_rebook', None):
                    self.ui.btn_rebook.setEnabled(is_owner)
            except Exception:
                pass
        except Exception:
            pass

    def rebook_selected(self):
        current_page = self.ui.stackedWidget.currentIndex()
        is_admin = current_page == 3
        table = self.ui.table_records_admin if is_admin else self.ui.table_records
        selection = table.selectedItems()
        if not selection:
            return QMessageBox.warning(self, "No Selection", "Select booking row first.")
        
        row = selection[0].row()
        booking_id = int(table.item(row, 0).text())
        
        conn, cursor = self.get_db_connection()
        if not conn:
            return
        cursor.execute("SELECT * FROM bookings WHERE id = %s", (booking_id,))
        booking = cursor.fetchone()
        conn.close()
        
        if not booking:
            return QMessageBox.warning(self, "Error", "Booking not found.")
        
        # Validation
        if self.logged_in and self.current_user.get('role') == 'customer' and booking['user_id'] != self.current_user.get('id'):
            return QMessageBox.warning(self, "Access Denied", "Only your own bookings.")
        
        reply = QMessageBox.question(self, 'Rebook?', f'Rebook ID {booking_id}?\nDates: {booking["checkin"]} - {booking["checkout"]}',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            reason, ok = QInputDialog.getText(self, 'Rebooking Reason', 'Reason (required):')
            if ok and reason.strip():
                # Prefill form
                self.ui.input_name.setText(booking['name'])
                if hasattr(self.ui, 'input_phone'):
                    self.ui.input_phone.setText(booking['phone'] or '')
                if hasattr(self.ui, 'input_email'):
                    self.ui.input_email.setText(booking['email'] or '')
                self.pending_rebook = {'from_id': booking_id, 'reason': reason}
                try:
                    self.ui.stackedWidget.setCurrentIndex(2)
                except Exception:
                    pass
                QMessageBox.information(self, "Prefilled", "Form prefilled with old data. Update dates/room and confirm to rebook.")
            else:
                QMessageBox.warning(self, "Rebook Cancelled", "Reason required.")

    def show_booking_details(self, item):
        """Show booking details in the form when a row is double-clicked (customer panel)."""
        try:
            row = item.row()
            table = self.ui.table_records
            booking_id = int(table.item(row, 0).text())
        except Exception:
            return

        conn, cursor = self.get_db_connection()
        if not conn:
            return
        try:
            cursor.execute("SELECT * FROM bookings WHERE id = %s", (booking_id,))
            booking = cursor.fetchone()
        except Exception:
            booking = None
        finally:
            conn.close()

        if not booking:
            return QMessageBox.warning(self, "Error", "Booking not found.")

        # Populate form fields for quick view/edit (do not change ownership)
        try:
            self.ui.input_name.setText(booking.get('name',''))
            if hasattr(self.ui, 'input_phone'):
                self.ui.input_phone.setText(booking.get('phone','') or '')
            if hasattr(self.ui, 'input_email'):
                self.ui.input_email.setText(booking.get('email','') or '')
            # Parse and set dates safely
            def _parse_booking_date(val):
                try:
                    if isinstance(val, str):
                        return date.fromisoformat(val)
                    if isinstance(val, datetime.datetime):
                        return val.date()
                    if isinstance(val, date):
                        return val
                except Exception:
                    pass
                try:
                    return date.fromisoformat(str(val))
                except Exception:
                    return date.today()

            checkin_dt = _parse_booking_date(booking.get('checkin'))
            checkout_dt = _parse_booking_date(booking.get('checkout'))
            try:
                self.ui.date_checkin.setDate(checkin_dt)
                self.ui.date_checkout.setDate(checkout_dt)
            except Exception:
                pass
            # Scroll to booking on the table and ensure selection
            try:
                self.ui.table_records.selectRow(row)
            except Exception:
                pass
            # Switch to booking form page if not already
            try:
                self.ui.stackedWidget.setCurrentIndex(2)
            except Exception:
                pass
        except Exception:
            pass

    def approve_selected_cancellation(self):
        print("approve_selected_cancellation called")
        # Approve the selected cancellation request (admin action)
        current_page = self.ui.stackedWidget.currentIndex()
        if current_page != 3:
            return QMessageBox.warning(self, "Not Admin", "Approve action is only available in Admin view.")
        table = self.ui.table_records_admin
        selection = table.selectedItems()
        if not selection:
            return QMessageBox.warning(self, "No Selection", "Select a booking row first.")
        row = selection[0].row()
        try:
            booking_id = int(table.item(row, 0).text())
        except Exception:
            return QMessageBox.warning(self, "Error", "Unable to determine booking ID.")

        conn, cursor = self.get_db_connection()
        if not conn:
            return QMessageBox.critical(self, "DB Error", "Cannot connect to database.")

        try:
            cursor.execute("SELECT status, cancellation_reason FROM bookings WHERE id = %s", (booking_id,))
            rowdata = cursor.fetchone()
            status = rowdata.get('status') if rowdata else None
            reason = rowdata.get('cancellation_reason') if rowdata else ''
            print(f"approve_selected_cancellation: booking_id={booking_id} db_row_exists={bool(rowdata)} status={status}")

            if status != 'Cancellation Requested':
                return QMessageBox.information(self, "Not Pending", f"Booking {booking_id} is not a cancellation request (status: {status}).")

            reply = QMessageBox.question(self, 'Approve Cancellation', f'Approve cancellation for booking {booking_id}?', QMessageBox.Yes | QMessageBox.No)
            if reply != QMessageBox.Yes:
                return

            # Mark as Cancelled and keep reason
            try:
                cursor.execute("UPDATE bookings SET status = 'Cancelled' WHERE id = %s", (booking_id,))
            except Exception as e:
                QMessageBox.critical(self, "DB Error", f"Failed to update booking: {e}")
                return
            self.refresh_table()
            QMessageBox.information(self, "Approved", f"Cancellation for booking {booking_id} approved.")
        finally:
            conn.close()
    
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
                    # Reveal admin user-management action
                    try:
                        if getattr(self.ui, 'btn_delete_admin', None):
                            self.ui.btn_delete_admin.setText('Delete User')
                            self.ui.btn_delete_admin.show()
                    except Exception:
                        pass
                else:
                    self.ui.stackedWidget.setCurrentIndex(2)
                    self.populate_customer_info()
                # Ensure action buttons reflect ownership state
                try:
                    self.update_action_buttons()
                except Exception:
                    pass
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
            try:
                self.update_action_buttons()
            except Exception:
                pass

    def on_page_changed(self, idx: int):
        """Page change security."""
        # When switching to admin page, ensure users are reloaded and tables refreshed
        try:
            if idx == 3:
                try:
                    self.auth_handler.users = self.auth_handler.load_users()
                except Exception:
                    pass
                self.refresh_table()
        except Exception:
            pass

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = FrontendApp()
    window.show()
    print("Hotel app running. Ensure XAMPP MySQL running & hotel_db.sql executed.")
    sys.exit(app.exec_())

