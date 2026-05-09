export const users = [
  {
    name: "Dr. Aisha Menon",
    email: "admin@collegeerp.com",
    password: "Admin@12345",
    role: "admin",
    department: "Administration",
    phone: "+91 90000 10001"
  },
  {
    name: "Prof. Kabir Sharma",
    email: "faculty@collegeerp.com",
    password: "Faculty@12345",
    role: "faculty",
    department: "Computer Science",
    phone: "+91 90000 10002"
  },
  {
    name: "Riya Patel",
    email: "student@collegeerp.com",
    password: "Student@12345",
    role: "student",
    department: "Computer Science",
    phone: "+91 90000 10003"
  }
];

export const records = {
  departments: [
    { code: "CSE", name: "Computer Science Engineering", head: "Prof. Kabir Sharma", building: "Innovation Block", intake: 240 },
    { code: "ECE", name: "Electronics & Communication", head: "Dr. Meera Iyer", building: "Tesla Block", intake: 180 },
    { code: "BBA", name: "Business Administration", head: "Dr. S. Banerjee", building: "Management Wing", intake: 160 }
  ],
  courses: [
    { code: "BTECH-CSE", title: "B.Tech Computer Science", department: "Computer Science", duration: "4 Years", credits: 164, fee: 145000 },
    { code: "BBA-AN", title: "BBA Business Analytics", department: "Business Administration", duration: "3 Years", credits: 128, fee: 96000 }
  ],
  subjects: [
    { code: "CS501", title: "Distributed Systems", course: "B.Tech Computer Science", semester: 5, faculty: "Prof. Kabir Sharma", credits: 4 },
    { code: "CS503", title: "Database Management Systems", course: "B.Tech Computer Science", semester: 5, faculty: "Dr. Nisha Rao", credits: 4 }
  ],
  students: [
    {
      rollNo: "CSE22001",
      name: "Riya Patel",
      email: "student@collegeerp.com",
      phone: "+91 90000 10003",
      department: "Computer Science",
      course: "B.Tech Computer Science",
      semester: 5,
      admissionDate: "2022-08-01",
      guardianName: "Mahesh Patel",
      address: "Ahmedabad, Gujarat"
    },
    {
      rollNo: "CSE22002",
      name: "Arjun Nair",
      email: "arjun.nair@example.com",
      phone: "+91 90000 10004",
      department: "Computer Science",
      course: "B.Tech Computer Science",
      semester: 5,
      admissionDate: "2022-08-01",
      guardianName: "Lakshmi Nair",
      address: "Kochi, Kerala"
    }
  ],
  faculty: [
    {
      employeeId: "FAC1001",
      name: "Prof. Kabir Sharma",
      email: "faculty@collegeerp.com",
      phone: "+91 90000 10002",
      designation: "Associate Professor",
      department: "Computer Science",
      specialization: "Cloud Computing"
    },
    {
      employeeId: "FAC1002",
      name: "Dr. Nisha Rao",
      email: "nisha.rao@example.com",
      phone: "+91 90000 10005",
      designation: "Assistant Professor",
      department: "Computer Science",
      specialization: "Data Engineering"
    }
  ],
  attendance: [
    { studentName: "Riya Patel", rollNo: "CSE22001", subject: "Distributed Systems", date: "2026-05-06", status: "Present", percentage: 92 },
    { studentName: "Arjun Nair", rollNo: "CSE22002", subject: "Database Management Systems", date: "2026-05-06", status: "Late", percentage: 84 }
  ],
  exams: [
    { title: "Mid Semester Examination", course: "B.Tech Computer Science", semester: 5, subject: "Distributed Systems", examDate: "2026-05-18", maxMarks: 50, venue: "Block A - 204" }
  ],
  results: [
    { rollNo: "CSE22001", studentName: "Riya Patel", exam: "Internal Assessment 1", subject: "Distributed Systems", marksObtained: 44, maxMarks: 50, grade: "A", remarks: "Excellent", published: true }
  ],
  fees: [
    { rollNo: "CSE22001", studentName: "Riya Patel", category: "Semester Fee", amount: 72500, paidAmount: 72500, dueDate: "2026-05-30", paymentStatus: "Paid", receiptNo: "RCPT-2026-001" },
    { rollNo: "CSE22002", studentName: "Arjun Nair", category: "Semester Fee", amount: 72500, paidAmount: 40000, dueDate: "2026-05-30", paymentStatus: "Partial", receiptNo: "RCPT-2026-002" }
  ],
  timetable: [
    { className: "CSE 5A", department: "Computer Science", day: "Monday", subject: "Distributed Systems", faculty: "Prof. Kabir Sharma", room: "Lab 3", startsAt: "09:00", endsAt: "10:00" },
    { className: "CSE 5A", department: "Computer Science", day: "Tuesday", subject: "DBMS", faculty: "Dr. Nisha Rao", room: "A-204", startsAt: "10:00", endsAt: "11:00" }
  ],
  notices: [
    { title: "Mid-semester hall tickets released", audience: "Students", body: "Students can download hall tickets from the exam portal.", priority: "High", publishDate: "2026-05-07" },
    { title: "Faculty development workshop", audience: "Faculty", body: "Workshop on AI-assisted curriculum design.", priority: "Normal", publishDate: "2026-05-09" }
  ],
  calendar: [
    { title: "Mid Semester Exams", type: "Exam", startDate: "2026-05-18", endDate: "2026-05-24", audience: "Students" },
    { title: "Annual Tech Fest", type: "Event", startDate: "2026-06-03", endDate: "2026-06-05", audience: "All" }
  ],
  assignments: [
    { title: "Consensus Protocol Case Study", subject: "Distributed Systems", faculty: "Prof. Kabir Sharma", dueDate: "2026-05-20", attachmentUrl: "/uploads/assignment.pdf", submissionCount: 76 }
  ],
  leaves: [
    { applicantName: "Riya Patel", role: "Student", fromDate: "2026-05-12", toDate: "2026-05-13", reason: "Medical appointment", status: "Pending" }
  ],
  grievances: [
    { submittedBy: "Arjun Nair", category: "Facilities", title: "Lab system maintenance", description: "Several systems in Lab 3 need keyboard replacement.", status: "In Review", priority: "Medium" }
  ],
  events: [
    { title: "HackSphere 2026", venue: "Auditorium", organizer: "CSE Association", eventDate: "2026-06-03", capacity: 600, registrations: 418 }
  ],
  library: [
    { accessionNo: "LIB-DS-001", title: "Designing Data-Intensive Applications", author: "Martin Kleppmann", category: "Computer Science", availableCopies: 6 },
    { accessionNo: "LIB-ALG-011", title: "Introduction to Algorithms", author: "CLRS", category: "Computer Science", availableCopies: 3, issuedTo: "CSE22001", dueDate: "2026-05-21" }
  ],
  hostel: [
    { hostelName: "Maple Residency", roomNo: "M-302", studentName: "Riya Patel", rollNo: "CSE22001", occupancyStatus: "Occupied", warden: "Ms. Elena Dsouza" }
  ],
  placements: [
    { company: "TCS Digital", role: "Software Engineer", packageLpa: 7.5, driveDate: "2026-06-15", eligibility: "CGPA 7.0+", registeredStudents: 210, selectedStudents: 0 }
  ],
  messages: [
    { from: "Admin Office", to: "All Students", subject: "Exam form correction window", body: "The correction window will remain open until 10 May 2026.", read: false }
  ],
  documents: [
    { ownerName: "Riya Patel", ownerRole: "Student", documentType: "Transfer Certificate", fileUrl: "/uploads/tc-riya.pdf", verificationStatus: "Verified", verifierNote: "Original verified." }
  ],
  performance: [
    { rollNo: "CSE22001", studentName: "Riya Patel", attendancePercentage: 92, cgpa: 8.8, assignmentScore: 91, riskLevel: "Low", advisorNote: "Strong performance." },
    { rollNo: "CSE22002", studentName: "Arjun Nair", attendancePercentage: 84, cgpa: 7.6, assignmentScore: 78, riskLevel: "Medium", advisorNote: "Needs assignment consistency." }
  ]
};
