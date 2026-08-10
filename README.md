# Trecking-Management-App
A Flask‑based web app built for the MAD‑1 project (IITM BS). It helps admins, trek staff, and trekkers manage treks, bookings, and trekking history using role‑based dashboards and an SQLite database.

## Technologies used:

- Python + Flask
- Jinja2 template
- SQLite3
- Plain HTML/CSS (no bootstrap)

## Important Note on Folder Structure
## FINAL PROJECT FOLDER UNDER THE FOLDER: final_25f2008303_tma_webapp
While uploading milestones to GitHub, a nesting issue occurred where each milestone upload created an extra nested folder inside the previous one, instead of updating files in place. Initially, a few files were deleted thinking it was a mistake, but this was stopped early on to avoid erasing the commit history of earlier milestones. As a result, the extra nested folders have been intentionally kept as-is to preserve milestone history.

**The latest, working version of the project is inside the 3rd nested folder level.** Please navigate three folders deep from the repository root to find the final `app.py`, `database.py`, and `templates/` folder to run the project.

## How to Run

1. Make sure Python is installed.
2. Install Flask through cmd prompt:
   ```
   pip install flask
   ```
3. Navigate to the 3rd nested folder (see note above) to find the latest `app.py`, `database.py`, and `templates/` folder. Place them together in one project folder if needed.
4. Run the app:
   ```
   python app.py
   ```
5. Open your browser at:
   ```
   http://127.0.0.1:5000/
   ```
6. The database file and tables are created automatically on first run, along with a default Admin account:
   - Email: `HA@tmawebapp.com`
   - Password: `admin@123321`

## Roles

- **Admin** — manage treks, approve/blacklist/remove staff, activate/deactivate users, view booking history.
- **Staff** — view assigned treks, update trek status, view trek participants.
- **User (Trekker)** — view available treks, book a trek, view active bookings, cancel a booking, view trek history, edit own profile.

## Issue Log:

### Milestone 1 - GitHub Setup
- Set up initial repo and folder structure.
- Nested folder issue started here due to repeated milestone uploads (see note above).

### Milestone 2 - Database Setup
- Created `users`, `staff`, `treks`, `bookings` tables.
- Fixed table creation order so foreign keys referenced existing tables.

### Milestone 3 - Authentication
- Added login/register routes.
- Fixed password check logic in login.
- Fixed duplicate email check during registration.

### Milestone 4 - Admin Dashboard / Trek Staff Dashboard (basic)
- Added trek add/edit/delete for Admin.
- Fixed broken redirect after trek status update.
- Added staff dashboard with assigned treks and a manage-trek page.

### Milestone 5 - User (Trekker) Dashboard
- Added available treks, current bookings, and booking history pages.
- Fixed available slots not decreasing on booking.
- Separated trek status (open/started/completed) from booking status to avoid conflicting logic.

### Milestone 6 - Booking Tracking / Final Cleanup
- Added Admin pages for staff management, user management, and booking history.
- Fixed staff deletion not removing the linked user account correctly.
- Added `is_active` check so deactivated users can't log in.
- Added staff `appstat` check (pending/approved/blacklisted) during login.
- Added a simple Edit Profile page for users (name, phone, password update).
- General cleanup of login, register, and home pages.

### Extra Milestone:
- Added a Edit users function in user dashboard.
  
### FINAL MILESTONE: 
- Fixed error in booking date not showing up in user bookings because of wrong sql query
- Uploaded entire folder again under name final_submission_tma_webapp

## Notes

- `app.secret_key` is used by Flask to sign session cookies, as an additional protection layer for secure login of admin, users and staff. It is set to a simple placeholder value since this is a local project.
