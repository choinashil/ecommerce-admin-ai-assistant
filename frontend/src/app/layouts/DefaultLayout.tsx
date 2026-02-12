import { Outlet } from 'react-router-dom';

import { Sidebar } from '@/widgets/sidebar';

const DefaultLayout = () => {
  return (
    <div className='flex h-screen'>
      <Sidebar />
      <main className='flex flex-1 overflow-hidden'>
        <Outlet />
      </main>
    </div>
  );
};

export default DefaultLayout;
