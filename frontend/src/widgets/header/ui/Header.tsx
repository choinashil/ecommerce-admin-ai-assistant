import ProfileMenu from './ProfileMenu';

const Header = () => {
  return (
    <header className='flex h-14 items-center justify-between border-b bg-background px-6'>
      <h1 className='text-2xl font-black'>SixPro</h1>
      <ProfileMenu />
    </header>
  );
};

export default Header;
