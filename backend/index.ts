import cors from "cors";
import express from "express";

import config from "./src/config/env";
import type { HttpError } from "./src/helpers/httpError";
import routes from "./src/routes/index.routes";

const app = express();

// Middleware globales
app.use(
  cors({
    origin: ["http://localhost:5173", "http://localhost:5174"],
    credentials: true,
  }),
);
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Rutas
app.use("/api", routes);

// Ruta de health check
app.get("/health", (req, res) => {
  res.json({ status: "OK", message: "Server is running" });
});

// Manejo de errores global
app.use(
  (
    err: HttpError | Error,
    req: express.Request,
    res: express.Response,
    _next: express.NextFunction,
  ) => {
    const status = "status" in err ? err.status : 500;
    const message = err.message || "Internal Server Error";

    res.status(status).json({
      error: {
        status,
        message,
        timestamp: new Date().toISOString(),
      },
    });
  },
);

// Manejo de rutas no encontradas
app.use((req, res) => {
  res.status(404).json({
    error: {
      status: 404,
      message: `Route ${req.originalUrl} not found`,
    },
  });
});

const PORT = config.port || 3000;

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📱 Health check: http://localhost:${PORT}/health`);
  console.log(`🔐 Auth routes: http://localhost:${PORT}/api/auth`);
});
