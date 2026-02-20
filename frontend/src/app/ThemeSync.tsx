import { useEffect } from 'react';
import { useLocation } from 'react-router-dom';

import { applyTheme } from '@/shared/lib/theme';

const ThemeSync = () => {
  const { pathname } = useLocation();

  useEffect(() => {
    applyTheme(pathname);
  }, [pathname]);

  return null;
};

export default ThemeSync;
