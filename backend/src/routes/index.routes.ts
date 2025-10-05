import { Router } from "express";

import authRoutes from "./auth.routes";

const router = Router();

// Rutas de autenticación
router.use("/auth", authRoutes);

export default router;
