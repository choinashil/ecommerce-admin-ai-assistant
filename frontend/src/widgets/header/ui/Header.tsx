import { Link } from 'react-router-dom';

import ProfileMenu from './ProfileMenu';

const Header = () => {
  return (
    <header className='flex h-14 items-center px-3'>
      <div className='mx-auto flex w-full max-w-7xl items-center justify-between'>
        <Link to='/' className='px-5 text-2xl font-black'>
          SixPro
        </Link>
        <ProfileMenu />
      </div>
    </header>
  );
};

export default Header;
