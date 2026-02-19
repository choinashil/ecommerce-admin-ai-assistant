import type { User, UserRole } from '../model/types';

export const USERS: User[] = [
  { id: 'seller-1', name: '판매자', role: 'seller' },
  { id: 'admin-1', name: '관리자', role: 'admin' },
];

export const DEFAULT_PATHS: Record<UserRole, string> = {
  seller: '/',
  admin: '/conversations',
};
