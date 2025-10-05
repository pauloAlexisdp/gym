export interface AuthControllerResponse<T = unknown> {
  success: boolean;
  message: string;
  data?: T;
}

export interface LoginControllerData {
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

export interface RegisterControllerData {
  id: number;
  name: string;
  lastname: string;
  email: string;
  role: string;
  isActive: boolean;
}

export interface ControllerError {
  statusCode: number;
  message: string;
  details?: string;
}
