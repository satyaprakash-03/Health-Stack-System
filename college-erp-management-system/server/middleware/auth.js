import jwt from "jsonwebtoken";
import { User } from "../models/User.js";
import { asyncHandler } from "./asyncHandler.js";

export const protect = asyncHandler(async (req, res, next) => {
  const authHeader = req.headers.authorization || "";
  const token = authHeader.startsWith("Bearer ") ? authHeader.split(" ")[1] : null;

  if (!token) {
    res.status(401);
    throw new Error("Authentication required.");
  }

  const decoded = jwt.verify(token, process.env.JWT_SECRET || "dev-secret");
  const user = await User.findById(decoded.id).select("-password");

  if (!user || !user.isActive) {
    res.status(401);
    throw new Error("User account is unavailable.");
  }

  req.user = user;
  next();
});

export const authorize = (...roles) => (req, res, next) => {
  if (!roles.includes(req.user.role)) {
    res.status(403);
    throw new Error("You do not have permission to access this resource.");
  }
  next();
};
