# EduSphere ERP - MERN College ERP Management System

EduSphere ERP is a production-oriented MERN scaffold for a professional college/university management portal. It includes role-based authentication, separate admin/faculty/student dashboards, reusable React components, MongoDB schemas, REST APIs, seed data, charts, tables, pagination, search, filtering, dark/light mode, and a responsive Bootstrap UI.

## Tech Stack

- Frontend: React, JavaScript, HTML, CSS, Bootstrap, Bootstrap Icons, Chart.js
- Backend: Node.js, Express.js, JWT, Multer, Nodemailer, Helmet, Rate Limiting
- Database: MongoDB with Mongoose models
- Architecture: MVC backend, reusable React components, REST API integration

## Folder Structure

```text
college-erp-management-system/
  client/
    src/
      components/       Reusable layout, tables, cards, modals, theme controls
      context/          Auth and theme provider
      data/             Role-aware module configuration
      pages/            Landing, login, dashboard, module CRUD, profile, reset pages
      routes/           Protected route guard
      services/         Axios API client with JWT handling
      styles/           Responsive Bootstrap-compatible UI styling
  server/
    config/             MongoDB and email configuration
    controllers/        Auth, dashboard, and generic CRUD controllers
    data/               Dummy data and database seeder
    middleware/         Auth, authorization, upload, async, and error middleware
    models/             User and ERP domain schemas
    routes/             Auth, dashboard, upload, and module REST routes
    server.js           Express app entrypoint
```

## ERP Modules Included

Student Management, Faculty Management, Departments, Courses, Subjects, Attendance, Exams, Results, Fees, Timetable, Notices, Academic Calendar, Assignments & Notes, Leave Applications, Grievances, Performance Analytics, Events, Library, Hostel, Placement & Training, Internal Messages, Profile Management, Password Reset, Email Notifications, Document Upload & Verification, and Admin Analytics.

Each module is available through:

```http
GET    /api/modules/:module
POST   /api/modules/:module
GET    /api/modules/:module/:id
PATCH  /api/modules/:module/:id
DELETE /api/modules/:module/:id
```

## Demo Accounts

After seeding MongoDB:

```text
Admin:   admin@collegeerp.com   / Admin@12345
Faculty: faculty@collegeerp.com / Faculty@12345
Student: student@collegeerp.com / Student@12345
```

## Setup

1. Copy `.env.example` to `.env` and update `MONGO_URI` and `JWT_SECRET`.
2. Install dependencies:

```bash
npm run install:all
```

3. Seed the database:

```bash
npm run seed
```

4. Run the full stack:

```bash
npm run dev
```

Frontend: `http://localhost:5173`

Backend: `http://localhost:5050/api`

## Notes For Production

- Use a strong `JWT_SECRET` and a managed MongoDB deployment.
- Configure SMTP variables for password reset and email notifications.
- Store uploads in object storage such as S3, Azure Blob, or Cloudinary for production.
- Add API-level audit logs and approval workflows for fees, results, and document verification.
- Add module-specific controllers if any workflow needs custom business rules beyond standard CRUD.
