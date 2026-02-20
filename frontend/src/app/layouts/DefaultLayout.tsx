import { useEffect } from 'react';
import { Outlet, useLocation } from 'react-router-dom';

import { applyTheme } from '@/shared/lib/theme';
import { Header } from '@/widgets/header';

const DefaultLayout = () => {
  const { pathname } = useLocation();

  useEffect(() => {
    applyTheme(pathname);
  }, [pathname]);

  return (
    <div className='flex h-screen flex-col'>
      <Header />
      <main className='flex flex-1 overflow-hidden'>
        <Outlet />
      </main>
    </div>
  );
};

export default DefaultLayout;
