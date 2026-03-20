# Hotel System SQL Update - TODO

## Approved Plan Steps:

1. [x] **Backup current DB/SQL**: Copied to hotel_db_backup.sql ✓
2. [x] **Create updated hotel_db.sql**: Created hotel_db_updated.sql with users/room_types/FKs/triggers ✓
3. [ ] **Execute SQL in MySQL**: Run hotel_db_updated.sql in phpMyAdmin
4. [ ] **Migrate data**: users.json -> users table, update bookings room_types
5. [ ] **Update main_frontend_fixed.py**: Adapt to new schema
6. [ ] **Update auth_handler.py**: DB backend
7. [ ] **Test full flow**
8. [ ] **Verify integrity**
9. [ ] **Update UI**
10. [x] **Final cleanup**: Remove TODO.md after all steps

**Current Progress**: Steps 1-2 complete. Next: Execute updated SQL (step 3).

**Next Command**: 
- Open phpMyAdmin (http://localhost/phpmyadmin)
- Import/Run c:/xampp/htdocs/hotel_system_adet/hotel_db_updated.sql
- Confirm tables: room_types, users, bookings (+view)

**Notes**:
- XAMPP MySQL must be running
- This replaces DB - backup done ✓
- Room IDs: 1=Standard($100), 2=Deluxe($250), 3=Suite($500)
