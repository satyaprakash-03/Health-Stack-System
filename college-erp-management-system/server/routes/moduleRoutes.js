import express from "express";
import { createItem, deleteItem, getItem, listItems, updateItem } from "../controllers/crudController.js";
import { protect } from "../middleware/auth.js";

const router = express.Router();

router.use(protect);
router.route("/:module").get(listItems).post(createItem);
router.route("/:module/:id").get(getItem).patch(updateItem).delete(deleteItem);

export default router;
