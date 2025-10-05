import type { Request, Response, NextFunction } from "express";

import type { AuthControllerResponse, LoginControllerData, RegisterControllerData } from "./auth.types";
import * as service from "../../service/auth/auth.service";

export async function register(
  req: Request,
  res: Response,
  next: NextFunction,
): Promise<Response | void> {
  try {
    const data = await service.register(req.body);
    const response: AuthControllerResponse<RegisterControllerData> = {
      success: true,
      message: "Usuario registrado exitosamente",
      data: data
    };
    return res.status(201).json(response);
  } catch (err) {
    return next(err);
  }
}

export async function login(
  req: Request,
  res: Response,
  next: NextFunction,
): Promise<Response | void> {
  try {
    const data = await service.login(req.body);
    const response: AuthControllerResponse<LoginControllerData> = {
      success: true,
      message: "Inicio de sesión exitoso",
      data: data
    };
    return res.json(response);
  } catch (err) {
    return next(err);
  }
}
