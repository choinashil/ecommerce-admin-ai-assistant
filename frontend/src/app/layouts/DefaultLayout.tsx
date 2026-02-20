import { Outlet } from 'react-router-dom';

import { Header } from '@/widgets/header';

const DefaultLayout = () => {
  return (
    <div className='flex h-screen flex-col bg-page'>
      <Header />
      <div className='flex min-h-0 flex-1 px-3'>
        <main className='mx-auto flex w-full max-w-7xl flex-1 gap-3 overflow-hidden'>
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DefaultLayout;
