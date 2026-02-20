import { Outlet } from 'react-router-dom';

import { Header } from '@/widgets/header';

const DefaultLayout = () => {
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
