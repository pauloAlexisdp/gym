export interface JWTClaims {
  sub: number;
  email: string;
  role: string;
  name: string;
  lastname: string;
  iat?: number;
  exp?: number;
}

export interface AuthServiceConfig {
  jwtSecret: string;
  tokenExpiry: string;
}

export interface UserRegistrationData {
  name: string;
  lastname: string;
  email: string;
  password: string;
  hashedPassword: string;
}

export interface LoginServiceResponse {
  token: string;
  user: {
    id: number;
    name: string;
    lastname: string;
    email: string;
    role: string;
    isActive: boolean;
  };
}

export interface RegisterServiceResponse {
  id: number;
  name: string;
  lastname: string;
  email: string;
  role: string;
  isActive: boolean;
}
