import { Link } from 'react-router-dom';

import ProfileMenu from './ProfileMenu';

const Header = () => {
  return (
    <header className='flex h-14 items-center justify-between border-b bg-background px-6'>
      <Link to='/' className='text-2xl font-black'>
        SixPro
      </Link>
      <ProfileMenu />
    </header>
  );
};

export default Header;
