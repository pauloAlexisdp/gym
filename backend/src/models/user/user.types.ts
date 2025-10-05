import type { User } from '@prisma/client';

export interface UserModelOperations {
  createUser: (data: CreateUserRequest) => Promise<User>;
  findByEmail: (email: string) => Promise<User | null>;
  findById: (id: number) => Promise<User | null>;
  updateUser: (id: number, data: UpdateUserRequest) => Promise<User>;
  deleteUser: (id: number) => Promise<void>;
}

export interface CreateUserRequest {
  name: string;
  lastname: string;
  email: string;
  password: string;
}

export interface UpdateUserRequest {
  name?: string;
  lastname?: string;
  email?: string;
  password?: string;
}

export interface UserQueryOptions {
  includePassword?: boolean;
  includeInactive?: boolean;
}

export interface UserSearchCriteria {
  email?: string;
  id?: number;
  isActive?: boolean;
}

export type UserModelResponse = User;
export type UserSafeResponse = Omit<User, 'password'>;
