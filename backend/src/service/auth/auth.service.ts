import jwt from "jsonwebtoken";

import type { JWTClaims, LoginServiceResponse, RegisterServiceResponse } from "./auth.types";
import config from "../../config/env";
import errors from "../../errors/auth.messages";
import { httpError } from "../../helpers/httpError";
import type {
  CreateUserRequest,
  LoginRequest,
} from "../../interfaces/auth.interface";
import { createUser, findByEmail } from "../../models/user/user.model";
import { hash, compare } from "../password.service";

function normalizeEmail(e: string): string {
  return e.trim().toLowerCase();
}

export async function register(args: CreateUserRequest): Promise<RegisterServiceResponse> {
  const normalizedEmail = normalizeEmail(args.email);

  const exists = await findByEmail(normalizedEmail);
  if (exists) throw httpError(409, errors.service.email_in_use);

  const hashed = await hash(args.password);

  const user = await createUser({
    name: args.name.trim(),
    lastname: args.lastname.trim(),
    email: normalizedEmail,
    password: hashed,
  });

  return {
    id: user.id,
    name: user.name,
    lastname: user.lastname,
    email: user.email,
    role: user.role,
    isActive: user.isActive,
  };
}

export async function login(args: LoginRequest): Promise<LoginServiceResponse> {
  const normalizedEmail = normalizeEmail(args.email);
  const user = await findByEmail(normalizedEmail);
  if (!user) throw httpError(400, errors.service.invalid_credentials);
  if (!user.isActive) throw httpError(403, errors.service.inactive_user);

  const ok = await compare(args.password, user.password);
  if (!ok) throw httpError(400, errors.service.invalid_credentials);

  const payload: JWTClaims = {
    sub: user.id,
    email: user.email,
    role: user.role,
    name: user.name,
    lastname: user.lastname,
  };

  const token = jwt.sign(payload, config.jwtSecret, { expiresIn: "1d" });

  return {
    token,
    user: {
      id: user.id,
      name: user.name,
      lastname: user.lastname,
      email: user.email,
      role: user.role,
      isActive: user.isActive,
    },
  };
}
