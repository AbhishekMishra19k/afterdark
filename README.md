# AFTERDARK — Django version

Nightlife event website for Indore, dark maroon/red/cream theme, with a
Django database backend, admin panel, and booking-confirmation emails.

**Important:** Vercel doesn't run Django (it's serverless, no persistent DB).
Since bhai ne ab Django + database + email maanga hai, deploy this on a
Django-friendly free host instead — **Railway**, **Render**, or **PythonAnywhere**
all work well and are just as fast to set up. Steps below use Railway/Render style
(`Procfile` already included).

## 1. Local setup

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env          # fill in SECRET_KEY, email creds etc.
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` for the site and `http://127.0.0.1:8000/admin/`
for the password-protected admin panel (login = the superuser you just created).

## 2. What to configure from the admin panel first

Go to `/admin/` → **Site Configuration** and set:
- **Event date & time** → drives the homepage countdown
- **Single/Couple pricing** (defaults ₹499 / ₹899)
- **Payment QR image** and/or **bank details** (shown to guest after they book)
- Venue, address, phone, email, Instagram, terms & conditions

Then add a few **Upcoming Events**, **Past Event Photos**, and **Reviews** so
the site doesn't look empty.

## 3. Email (booking confirmation)

By default emails just print to the console (`EMAIL_BACKEND=console`) — fine
for local testing. For real emails, set these in `.env` (Gmail example, use an
**App Password**, not your normal Gmail password):

```
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=youraddress@gmail.com
EMAIL_HOST_PASSWORD=your-16-char-app-password
DEFAULT_FROM_EMAIL=AFTERDARK <youraddress@gmail.com>
```

A confirmation email is sent automatically the moment someone submits the
booking form (before payment) — with booking ID, amount due, and the 18+/ID
reminder.

## 4. Database

- Local dev: SQLite (zero setup, file-based).
- Production: set `DATABASE_URL` in `.env` to a Postgres instance — free
  options: **Supabase**, **Neon**, or Railway's built-in Postgres plugin.
  The app auto-switches to it when `DATABASE_URL` is present.

## 5. Deploy (Railway example — free tier, fast)

```bash
npm i -g @railway/cli      # or use the Railway web dashboard
railway login
railway init
railway up
```

Then in the Railway dashboard:
1. Add a Postgres plugin → it auto-injects `DATABASE_URL`.
2. Add env vars from `.env.example` (`SECRET_KEY`, `EMAIL_*`, `ALLOWED_HOSTS`
   = your `*.up.railway.app` domain).
3. Railway runs `release: python manage.py migrate` automatically (see
   `Procfile`), then starts `gunicorn`.
4. Visit the generated URL, then `/admin/` to log in and configure the site
   (step 2 above).

Render.com works the same way (Procfile + env vars); PythonAnywhere needs a
couple of manual WSGI steps but also works fine for a low-traffic site like this.

## 6. Bookings — view & export

`/admin/` → **Bookings** shows every booking (name, age, email, location,
entry type, price, payment status). Select rows → **Export selected bookings
to CSV** for a spreadsheet download.

## 7. Notes on what's enforced

- Age < 18 is rejected server-side in the booking form (`clean_age`).
- Entry type is limited to Single/Couple only — no group option exists in
  the form or model, so group bookings can't be submitted.
- Payment: admin uploads a QR image and/or types bank details in
  **Site Configuration**; guest submits a payment reference (UTR/UPI ID)
  after paying. Optionally set a Razorpay Payment Link for one-click
  online checkout too — toggle `razorpay_enabled` and paste the link.
