export const roleLabels = {
  admin: "Admin",
  faculty: "Faculty",
  student: "Student"
};

export const modules = [
  { key: "students", label: "Students", icon: "bi-mortarboard", roles: ["admin", "faculty"], fields: ["rollNo", "name", "department", "course", "semester", "status"] },
  { key: "faculty", label: "Faculty", icon: "bi-person-workspace", roles: ["admin"], fields: ["employeeId", "name", "department", "designation", "status"] },
  { key: "departments", label: "Departments", icon: "bi-buildings", roles: ["admin"], fields: ["code", "name", "head", "intake", "status"] },
  { key: "courses", label: "Courses", icon: "bi-journal-bookmark", roles: ["admin", "faculty"], fields: ["code", "title", "department", "duration", "credits", "fee"] },
  { key: "subjects", label: "Subjects", icon: "bi-book", roles: ["admin", "faculty"], fields: ["code", "title", "course", "semester", "faculty", "credits"] },
  { key: "attendance", label: "Attendance", icon: "bi-calendar-check", roles: ["admin", "faculty", "student"], fields: ["rollNo", "studentName", "subject", "status", "percentage"] },
  { key: "exams", label: "Exams", icon: "bi-pencil-square", roles: ["admin", "faculty", "student"], fields: ["title", "course", "subject", "examDate", "maxMarks", "status"] },
  { key: "results", label: "Results", icon: "bi-award", roles: ["admin", "faculty", "student"], fields: ["rollNo", "studentName", "subject", "marksObtained", "grade", "published"] },
  { key: "fees", label: "Fees", icon: "bi-credit-card", roles: ["admin", "student"], fields: ["rollNo", "studentName", "category", "amount", "paidAmount", "paymentStatus"] },
  { key: "timetable", label: "Timetable", icon: "bi-clock-history", roles: ["admin", "faculty", "student"], fields: ["className", "day", "subject", "faculty", "room", "startsAt"] },
  { key: "notices", label: "Notices", icon: "bi-megaphone", roles: ["admin", "faculty", "student"], fields: ["title", "audience", "priority", "publishDate"] },
  { key: "calendar", label: "Academic Calendar", icon: "bi-calendar3", roles: ["admin", "faculty", "student"], fields: ["title", "type", "startDate", "endDate", "audience"] },
  { key: "assignments", label: "Assignments & Notes", icon: "bi-cloud-arrow-up", roles: ["admin", "faculty", "student"], fields: ["title", "subject", "faculty", "dueDate", "submissionCount", "status"] },
  { key: "leaves", label: "Leave Applications", icon: "bi-send", roles: ["admin", "faculty", "student"], fields: ["applicantName", "role", "fromDate", "toDate", "status"] },
  { key: "grievances", label: "Grievances", icon: "bi-shield-exclamation", roles: ["admin", "faculty", "student"], fields: ["submittedBy", "category", "title", "status", "priority"] },
  { key: "performance", label: "Performance", icon: "bi-graph-up-arrow", roles: ["admin", "faculty", "student"], fields: ["rollNo", "studentName", "attendancePercentage", "cgpa", "assignmentScore", "riskLevel"] },
  { key: "events", label: "Events", icon: "bi-stars", roles: ["admin", "faculty", "student"], fields: ["title", "venue", "organizer", "eventDate", "registrations", "status"] },
  { key: "library", label: "Library", icon: "bi-bookshelf", roles: ["admin", "faculty", "student"], fields: ["accessionNo", "title", "author", "category", "availableCopies", "issuedTo"] },
  { key: "hostel", label: "Hostel", icon: "bi-house-door", roles: ["admin", "student"], fields: ["hostelName", "roomNo", "studentName", "rollNo", "occupancyStatus"] },
  { key: "placements", label: "Placement & Training", icon: "bi-briefcase", roles: ["admin", "faculty", "student"], fields: ["company", "role", "packageLpa", "driveDate", "registeredStudents", "status"] },
  { key: "messages", label: "Messages", icon: "bi-chat-left-text", roles: ["admin", "faculty", "student"], fields: ["from", "to", "subject", "read"] },
  { key: "documents", label: "Documents", icon: "bi-file-earmark-check", roles: ["admin", "faculty", "student"], fields: ["ownerName", "ownerRole", "documentType", "verificationStatus"] }
];

export const canEdit = (role) => ["admin", "faculty"].includes(role);
