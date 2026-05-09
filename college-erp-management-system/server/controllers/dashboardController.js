import { MODULES } from "./crudController.js";
import { asyncHandler } from "../middleware/asyncHandler.js";

export const dashboardSummary = asyncHandler(async (req, res) => {
  const counts = {};

  await Promise.all(
    Object.entries(MODULES).map(async ([key, entry]) => {
      if (entry.roles.includes(req.user.role)) counts[key] = await entry.model.countDocuments();
    })
  );

  res.json({
    role: req.user.role,
    counts,
    finance: {
      collected: 8240000,
      pending: 1160000,
      scholarship: 640000
    },
    performance: [
      { label: "Attendance", value: 88 },
      { label: "Assignments", value: 79 },
      { label: "Exam Pass Rate", value: 92 },
      { label: "Placement Readiness", value: 74 }
    ],
    trend: [
      { month: "Jan", students: 920, attendance: 84 },
      { month: "Feb", students: 955, attendance: 86 },
      { month: "Mar", students: 978, attendance: 88 },
      { month: "Apr", students: 1014, attendance: 89 },
      { month: "May", students: 1032, attendance: 91 }
    ],
    upcoming: [
      { title: "Mid-semester examination", date: "2026-05-18", type: "Exam" },
      { title: "Placement readiness workshop", date: "2026-05-22", type: "Training" },
      { title: "Annual technology fest", date: "2026-06-03", type: "Event" }
    ]
  });
});
