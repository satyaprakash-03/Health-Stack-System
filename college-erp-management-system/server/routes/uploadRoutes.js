import express from "express";
import { upload } from "../middleware/upload.js";
import { protect } from "../middleware/auth.js";

const router = express.Router();

router.post("/", protect, upload.single("file"), (req, res) => {
  res.status(201).json({
    message: "File uploaded successfully.",
    fileUrl: `/uploads/${req.file.filename}`,
    originalName: req.file.originalname
  });
});

export default router;
