import express from "express";
import { forgotPassword, login, me, register, resetPassword, updateProfile } from "../controllers/authController.js";
import { protect, authorize } from "../middleware/auth.js";

const router = express.Router();

router.post("/login", login);
router.post("/register", protect, authorize("admin"), register);
router.get("/me", protect, me);
router.patch("/profile", protect, updateProfile);
router.post("/forgot-password", forgotPassword);
router.patch("/reset-password/:token", resetPassword);

export default router;
