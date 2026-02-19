import type { UserRole } from '@/entities/user';

export const applyTheme = (role: UserRole) => {
  if (role === 'admin') {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
};
