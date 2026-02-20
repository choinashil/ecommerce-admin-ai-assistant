import { isAdminPath } from '@/shared/config/routes';

export const applyTheme = (pathname: string) => {
  if (isAdminPath(pathname)) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
};
