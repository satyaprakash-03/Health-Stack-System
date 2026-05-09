import crypto from "crypto";
import jwt from "jsonwebtoken";
import { asyncHandler } from "../middleware/asyncHandler.js";
import { sendEmail } from "../config/mail.js";
import { User } from "../models/User.js";

const signToken = (user) =>
  jwt.sign({ id: user._id, role: user.role }, process.env.JWT_SECRET || "dev-secret", {
    expiresIn: process.env.JWT_EXPIRES_IN || "7d"
  });

const sendAuthResponse = (res, user, statusCode = 200) => {
  const token = signToken(user);
  res.status(statusCode).json({
    token,
    user: {
      id: user._id,
      name: user.name,
      email: user.email,
      role: user.role,
      department: user.department,
      avatar: user.avatar
    }
  });
};

export const register = asyncHandler(async (req, res) => {
  const { name, email, password, role = "student", department, phone } = req.body;
  const existing = await User.findOne({ email });

  if (existing) {
    res.status(409);
    throw new Error("A user already exists with this email.");
  }

  const user = await User.create({ name, email, password, role, department, phone });
  sendAuthResponse(res, user, 201);
});

export const login = asyncHandler(async (req, res) => {
  const { email, password } = req.body;
  const user = await User.findOne({ email }).select("+password");

  if (!user || !(await user.matchPassword(password))) {
    res.status(401);
    throw new Error("Invalid email or password.");
  }

  sendAuthResponse(res, user);
});

export const me = asyncHandler(async (req, res) => {
  res.json({ user: req.user });
});

export const updateProfile = asyncHandler(async (req, res) => {
  const allowed = ["name", "phone", "department", "avatar"];
  allowed.forEach((field) => {
    if (req.body[field] !== undefined) req.user[field] = req.body[field];
  });
  const user = await req.user.save();
  res.json({ user });
});

export const forgotPassword = asyncHandler(async (req, res) => {
  const user = await User.findOne({ email: req.body.email });

  if (!user) {
    res.json({ message: "If that email exists, a reset link has been sent." });
    return;
  }

  const resetToken = user.createPasswordResetToken();
  await user.save({ validateBeforeSave: false });

  const resetUrl = `${process.env.CLIENT_URL || "http://localhost:5173"}/reset-password/${resetToken}`;
  await sendEmail({
    to: user.email,
    subject: "Reset your College ERP password",
    html: `<p>Hello ${user.name},</p><p>Use this secure link to reset your password:</p><p><a href="${resetUrl}">${resetUrl}</a></p>`
  });

  res.json({ message: "If that email exists, a reset link has been sent." });
});

export const resetPassword = asyncHandler(async (req, res) => {
  const hashedToken = crypto.createHash("sha256").update(req.params.token).digest("hex");
  const user = await User.findOne({
    resetPasswordToken: hashedToken,
    resetPasswordExpires: { $gt: Date.now() }
  }).select("+password");

  if (!user) {
    res.status(400);
    throw new Error("Password reset token is invalid or expired.");
  }

  user.password = req.body.password;
  user.resetPasswordToken = undefined;
  user.resetPasswordExpires = undefined;
  await user.save();

  sendAuthResponse(res, user);
});
