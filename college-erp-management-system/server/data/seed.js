import dotenv from "dotenv";
import { connectDB } from "../config/db.js";
import { User } from "../models/User.js";
import { MODULES } from "../controllers/crudController.js";
import { records, users } from "./dummyData.js";

dotenv.config();
await connectDB();

const seed = async () => {
  await User.deleteMany();
  await Promise.all(Object.values(MODULES).map(({ model }) => model.deleteMany()));

  for (const user of users) {
    await User.create(user);
  }

  for (const [moduleName, moduleRecords] of Object.entries(records)) {
    const entry = MODULES[moduleName];
    if (entry) await entry.model.insertMany(moduleRecords);
  }

  console.log("College ERP dummy data inserted.");
  console.log("Admin: admin@collegeerp.com / Admin@12345");
  console.log("Faculty: faculty@collegeerp.com / Faculty@12345");
  console.log("Student: student@collegeerp.com / Student@12345");
  process.exit(0);
};

seed().catch((error) => {
  console.error(error);
  process.exit(1);
});
