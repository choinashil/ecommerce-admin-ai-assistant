export type UserRole = 'seller' | 'admin';

export interface User {
  id: string;
  name: string;
  role: UserRole;
}
