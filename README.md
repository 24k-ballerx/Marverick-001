# Secondary School Portal & Website

Complete page structure and system linking: **Public Website** (external) and **School Portal** (internal, role-based).

## Architecture

- **Users** → **Frontend (HTML/CSS/JS)** → **Backend (Python/Django)** → **MySQL** (or SQLite for dev) → Hosting & Backup

## Quick start (SQLite – no MySQL required)

```bash
cd "c:\Users\USER\Marverick 001"
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
set USE_SQLITE=true
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- **Public site:** http://127.0.0.1:8000/  
- **Portal login:** http://127.0.0.1:8000/portal/login/  
- **Django Admin:** http://127.0.0.1:8000/admin/  

To use portal roles, create users in Django Admin and set **role** to Admin, Teacher, or Student. Create **Teacher** / **Student** profiles and link them to those users.

## Using MySQL

1. Create a database, e.g. `school_portal`.
2. Set (or export) environment variables:
   - `DB_NAME=school_portal`
   - `DB_USER=your_user`
   - `DB_PASSWORD=your_password`
   - `DB_HOST=127.0.0.1`
   - `DB_PORT=3306`
3. Do **not** set `USE_SQLITE`.
4. Run `pip install mysqlclient` and `python manage.py migrate`.

## Part 1: Public Website (External)

| Page               | Purpose                          | Links / Actions                          |
|--------------------|----------------------------------|------------------------------------------|
| Home               | Landing                          | About, Academics, Admissions, News, Contact, Portal Login |
| About Us           | School info                      | Academics, Admissions, Contact          |
| Academics          | Programs                         | Admissions, Contact                      |
| Admissions         | How to apply                     | Online Application, Contact             |
| Online Application | Apply online                     | Submits to **Admin Admissions Queue**    |
| News & Events      | List/detail                      | Links to individual news pages           |
| Contact            | Contact form                     | Submits to **Admin** (ContactMessage)    |
| Portal Login       | Entry to portal                  | Redirects to **Role-Based Dashboard**    |

## Part 2: School Portal (Internal)

### Admin

- **Admin Dashboard** → Student Management, Teacher Management, Classes & Subjects, Results, Announcements, Admissions Queue, Settings, Contact messages.
- **Student Management** → Student profile, academic history, results.
- **Teacher Management** → Teacher profile, assigned classes.
- **Class & Subject Management** → Student lists, results upload.
- **Results Management** → Approve results → visible to students.
- **Announcements** → Published to dashboards.
- **Admissions Queue** → Approve/Reject → can convert to student record (via Admin).
- **Settings** → Academic session, grading (via Admin), roles & permissions.

### Teacher

- **Teacher Dashboard** → My Classes, Upload Results, Announcements.
- **Upload Results** → Submitted to Admin for approval.
- **View Students** → Class-based student list.

### Student

- **Student Dashboard** → My Results, Announcements.
- **My Results** → Filter by term & session, print.
- **Announcements** → School-wide and class-specific notices.

## UI

- **Public site:** Blue/white header, hero, cards, clear nav and footer.
- **Portal:** Dark blue header, left sidebar, summary cards, tables, forms (aligned with your reference UI).

## Files overview

- `config/` – Django settings, root URLs.
- `public/` – Public website views and URLs.
- `portal/` – Portal app: auth, dashboards, admin/teacher/student flows, models, forms.
- `templates/` – Base (public + portal), public pages, portal role-specific pages.
- `static/css/` – `public.css`, `portal.css`.
