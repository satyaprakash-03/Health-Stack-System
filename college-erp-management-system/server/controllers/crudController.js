import {
  AcademicCalendar,
  Assignment,
  Attendance,
  Course,
  Department,
  Document,
  Event,
  Exam,
  Faculty,
  Fee,
  Grievance,
  Hostel,
  Leave,
  Library,
  Message,
  Notice,
  Performance,
  Placement,
  Result,
  Student,
  Subject,
  Timetable
} from "../models/CollegeModels.js";
import { asyncHandler } from "../middleware/asyncHandler.js";

export const MODULES = {
  students: { model: Student, roles: ["admin", "faculty"] },
  faculty: { model: Faculty, roles: ["admin"] },
  departments: { model: Department, roles: ["admin"] },
  courses: { model: Course, roles: ["admin", "faculty"] },
  subjects: { model: Subject, roles: ["admin", "faculty"] },
  attendance: { model: Attendance, roles: ["admin", "faculty", "student"] },
  exams: { model: Exam, roles: ["admin", "faculty", "student"] },
  results: { model: Result, roles: ["admin", "faculty", "student"] },
  fees: { model: Fee, roles: ["admin", "student"] },
  timetable: { model: Timetable, roles: ["admin", "faculty", "student"] },
  notices: { model: Notice, roles: ["admin", "faculty", "student"] },
  calendar: { model: AcademicCalendar, roles: ["admin", "faculty", "student"] },
  assignments: { model: Assignment, roles: ["admin", "faculty", "student"] },
  leaves: { model: Leave, roles: ["admin", "faculty", "student"] },
  grievances: { model: Grievance, roles: ["admin", "faculty", "student"] },
  events: { model: Event, roles: ["admin", "faculty", "student"] },
  library: { model: Library, roles: ["admin", "faculty", "student"] },
  hostel: { model: Hostel, roles: ["admin", "student"] },
  placements: { model: Placement, roles: ["admin", "faculty", "student"] },
  messages: { model: Message, roles: ["admin", "faculty", "student"] },
  documents: { model: Document, roles: ["admin", "faculty", "student"] },
  performance: { model: Performance, roles: ["admin", "faculty", "student"] }
};

const getModule = (req) => {
  const entry = MODULES[req.params.module];
  if (!entry) {
    const error = new Error("Unknown ERP module.");
    error.statusCode = 404;
    throw error;
  }
  if (!entry.roles.includes(req.user.role)) {
    const error = new Error("This role cannot access the requested module.");
    error.statusCode = 403;
    throw error;
  }
  return entry;
};

const buildQuery = (req) => {
  const { search, status, department, role } = req.query;
  const query = {};

  if (status) query.status = status;
  if (department) query.department = department;
  if (role) query.role = role;

  if (search) {
    query.$or = [
      { name: { $regex: search, $options: "i" } },
      { title: { $regex: search, $options: "i" } },
      { studentName: { $regex: search, $options: "i" } },
      { rollNo: { $regex: search, $options: "i" } },
      { code: { $regex: search, $options: "i" } },
      { company: { $regex: search, $options: "i" } }
    ];
  }

  return query;
};

export const listItems = asyncHandler(async (req, res) => {
  const { model } = getModule(req);
  const page = Math.max(Number(req.query.page || 1), 1);
  const limit = Math.min(Number(req.query.limit || 10), 50);
  const skip = (page - 1) * limit;
  const query = buildQuery(req);

  const [items, total] = await Promise.all([
    model.find(query).sort({ createdAt: -1 }).skip(skip).limit(limit),
    model.countDocuments(query)
  ]);

  res.json({
    items,
    pagination: {
      page,
      limit,
      total,
      pages: Math.ceil(total / limit) || 1
    }
  });
});

export const getItem = asyncHandler(async (req, res) => {
  const { model } = getModule(req);
  const item = await model.findById(req.params.id);
  if (!item) {
    res.status(404);
    throw new Error("Record not found.");
  }
  res.json({ item });
});

export const createItem = asyncHandler(async (req, res) => {
  const { model } = getModule(req);
  const item = await model.create({ ...req.body, createdBy: req.user._id });
  res.status(201).json({ item });
});

export const updateItem = asyncHandler(async (req, res) => {
  const { model } = getModule(req);
  const item = await model.findByIdAndUpdate(
    req.params.id,
    { ...req.body, updatedBy: req.user._id },
    { new: true, runValidators: true }
  );

  if (!item) {
    res.status(404);
    throw new Error("Record not found.");
  }

  res.json({ item });
});

export const deleteItem = asyncHandler(async (req, res) => {
  const { model } = getModule(req);
  const item = await model.findByIdAndDelete(req.params.id);

  if (!item) {
    res.status(404);
    throw new Error("Record not found.");
  }

  res.json({ message: "Record deleted successfully." });
});
