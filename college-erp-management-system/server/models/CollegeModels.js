import mongoose from "mongoose";

const { Schema, model } = mongoose;

const auditFields = {
  createdBy: { type: Schema.Types.ObjectId, ref: "User" },
  updatedBy: { type: Schema.Types.ObjectId, ref: "User" }
};

const studentSchema = new Schema(
  {
    rollNo: { type: String, required: true, unique: true },
    name: { type: String, required: true },
    email: { type: String, required: true },
    phone: String,
    department: String,
    course: String,
    semester: Number,
    admissionDate: Date,
    status: { type: String, enum: ["Active", "Alumni", "Suspended"], default: "Active" },
    guardianName: String,
    address: String,
    ...auditFields
  },
  { timestamps: true }
);

const facultySchema = new Schema(
  {
    employeeId: { type: String, required: true, unique: true },
    name: { type: String, required: true },
    email: { type: String, required: true },
    phone: String,
    designation: String,
    department: String,
    specialization: String,
    status: { type: String, enum: ["Active", "On Leave", "Inactive"], default: "Active" },
    ...auditFields
  },
  { timestamps: true }
);

const departmentSchema = new Schema(
  {
    code: { type: String, required: true, unique: true },
    name: { type: String, required: true },
    head: String,
    building: String,
    intake: Number,
    status: { type: String, enum: ["Active", "Inactive"], default: "Active" },
    ...auditFields
  },
  { timestamps: true }
);

const courseSchema = new Schema(
  {
    code: { type: String, required: true, unique: true },
    title: { type: String, required: true },
    department: String,
    duration: String,
    credits: Number,
    fee: Number,
    status: { type: String, enum: ["Open", "Closed"], default: "Open" },
    ...auditFields
  },
  { timestamps: true }
);

const subjectSchema = new Schema(
  {
    code: { type: String, required: true, unique: true },
    title: { type: String, required: true },
    course: String,
    semester: Number,
    faculty: String,
    credits: Number,
    ...auditFields
  },
  { timestamps: true }
);

const attendanceSchema = new Schema(
  {
    studentName: String,
    rollNo: String,
    subject: String,
    date: Date,
    status: { type: String, enum: ["Present", "Absent", "Late"], default: "Present" },
    percentage: Number,
    ...auditFields
  },
  { timestamps: true }
);

const examSchema = new Schema(
  {
    title: { type: String, required: true },
    course: String,
    semester: Number,
    subject: String,
    examDate: Date,
    maxMarks: Number,
    venue: String,
    status: { type: String, enum: ["Scheduled", "Completed", "Cancelled"], default: "Scheduled" },
    ...auditFields
  },
  { timestamps: true }
);

const resultSchema = new Schema(
  {
    rollNo: String,
    studentName: String,
    exam: String,
    subject: String,
    marksObtained: Number,
    maxMarks: Number,
    grade: String,
    remarks: String,
    published: { type: Boolean, default: false },
    ...auditFields
  },
  { timestamps: true }
);

const feeSchema = new Schema(
  {
    rollNo: String,
    studentName: String,
    category: String,
    amount: Number,
    paidAmount: Number,
    dueDate: Date,
    paymentStatus: { type: String, enum: ["Paid", "Partial", "Pending", "Overdue"], default: "Pending" },
    receiptNo: String,
    ...auditFields
  },
  { timestamps: true }
);

const timetableSchema = new Schema(
  {
    className: String,
    department: String,
    day: String,
    subject: String,
    faculty: String,
    room: String,
    startsAt: String,
    endsAt: String,
    ...auditFields
  },
  { timestamps: true }
);

const noticeSchema = new Schema(
  {
    title: { type: String, required: true },
    audience: { type: String, enum: ["All", "Faculty", "Students", "Admin"], default: "All" },
    body: String,
    priority: { type: String, enum: ["Normal", "High", "Urgent"], default: "Normal" },
    publishDate: Date,
    expiresAt: Date,
    ...auditFields
  },
  { timestamps: true }
);

const academicCalendarSchema = new Schema(
  {
    title: { type: String, required: true },
    type: { type: String, enum: ["Holiday", "Exam", "Event", "Registration", "Academic"], default: "Academic" },
    startDate: Date,
    endDate: Date,
    audience: String,
    ...auditFields
  },
  { timestamps: true }
);

const assignmentSchema = new Schema(
  {
    title: { type: String, required: true },
    subject: String,
    faculty: String,
    dueDate: Date,
    attachmentUrl: String,
    submissionCount: Number,
    status: { type: String, enum: ["Draft", "Published", "Closed"], default: "Published" },
    ...auditFields
  },
  { timestamps: true }
);

const leaveSchema = new Schema(
  {
    applicantName: String,
    role: { type: String, enum: ["Student", "Faculty"], default: "Student" },
    fromDate: Date,
    toDate: Date,
    reason: String,
    status: { type: String, enum: ["Pending", "Approved", "Rejected"], default: "Pending" },
    reviewerNote: String,
    ...auditFields
  },
  { timestamps: true }
);

const grievanceSchema = new Schema(
  {
    submittedBy: String,
    category: String,
    title: { type: String, required: true },
    description: String,
    status: { type: String, enum: ["Open", "In Review", "Resolved", "Closed"], default: "Open" },
    priority: { type: String, enum: ["Low", "Medium", "High"], default: "Medium" },
    ...auditFields
  },
  { timestamps: true }
);

const eventSchema = new Schema(
  {
    title: { type: String, required: true },
    venue: String,
    organizer: String,
    eventDate: Date,
    capacity: Number,
    registrations: Number,
    status: { type: String, enum: ["Upcoming", "Completed", "Cancelled"], default: "Upcoming" },
    ...auditFields
  },
  { timestamps: true }
);

const librarySchema = new Schema(
  {
    accessionNo: { type: String, required: true, unique: true },
    title: { type: String, required: true },
    author: String,
    category: String,
    availableCopies: Number,
    issuedTo: String,
    dueDate: Date,
    ...auditFields
  },
  { timestamps: true }
);

const hostelSchema = new Schema(
  {
    hostelName: String,
    roomNo: String,
    studentName: String,
    rollNo: String,
    occupancyStatus: { type: String, enum: ["Vacant", "Occupied", "Maintenance"], default: "Occupied" },
    warden: String,
    ...auditFields
  },
  { timestamps: true }
);

const placementSchema = new Schema(
  {
    company: { type: String, required: true },
    role: String,
    packageLpa: Number,
    driveDate: Date,
    eligibility: String,
    registeredStudents: Number,
    selectedStudents: Number,
    status: { type: String, enum: ["Open", "Completed", "Cancelled"], default: "Open" },
    ...auditFields
  },
  { timestamps: true }
);

const messageSchema = new Schema(
  {
    from: String,
    to: String,
    subject: String,
    body: String,
    read: { type: Boolean, default: false },
    ...auditFields
  },
  { timestamps: true }
);

const documentSchema = new Schema(
  {
    ownerName: String,
    ownerRole: { type: String, enum: ["Student", "Faculty"], default: "Student" },
    documentType: String,
    fileUrl: String,
    verificationStatus: { type: String, enum: ["Pending", "Verified", "Rejected"], default: "Pending" },
    verifierNote: String,
    ...auditFields
  },
  { timestamps: true }
);

const performanceSchema = new Schema(
  {
    rollNo: String,
    studentName: String,
    attendancePercentage: Number,
    cgpa: Number,
    assignmentScore: Number,
    riskLevel: { type: String, enum: ["Low", "Medium", "High"], default: "Low" },
    advisorNote: String,
    ...auditFields
  },
  { timestamps: true }
);

export const Student = model("Student", studentSchema);
export const Faculty = model("Faculty", facultySchema);
export const Department = model("Department", departmentSchema);
export const Course = model("Course", courseSchema);
export const Subject = model("Subject", subjectSchema);
export const Attendance = model("Attendance", attendanceSchema);
export const Exam = model("Exam", examSchema);
export const Result = model("Result", resultSchema);
export const Fee = model("Fee", feeSchema);
export const Timetable = model("Timetable", timetableSchema);
export const Notice = model("Notice", noticeSchema);
export const AcademicCalendar = model("AcademicCalendar", academicCalendarSchema);
export const Assignment = model("Assignment", assignmentSchema);
export const Leave = model("Leave", leaveSchema);
export const Grievance = model("Grievance", grievanceSchema);
export const Event = model("Event", eventSchema);
export const Library = model("Library", librarySchema);
export const Hostel = model("Hostel", hostelSchema);
export const Placement = model("Placement", placementSchema);
export const Message = model("Message", messageSchema);
export const Document = model("Document", documentSchema);
export const Performance = model("Performance", performanceSchema);
