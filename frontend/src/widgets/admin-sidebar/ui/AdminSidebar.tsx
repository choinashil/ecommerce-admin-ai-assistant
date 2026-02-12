import { NavLink } from 'react-router-dom';

import { LayoutDashboard, FileText } from 'lucide-react';

import { cn } from '@/shared/lib/utils';

const NAV_ITEMS = [
  { to: '/', label: '대시보드', icon: LayoutDashboard },
  { to: '/logs', label: 'LLM 로그', icon: FileText },
];

const AdminSidebar = () => {
  return (
    <aside className='flex w-52 flex-col border-r bg-muted/40 p-4'>
      <h2 className='mb-6 text-lg font-semibold'>Admin</h2>
      <nav className='flex flex-col gap-1'>
        {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-2 rounded-md px-3 py-2 text-sm transition-colors',
                isActive ? 'bg-primary text-primary-foreground' : 'hover:bg-muted',
              )
            }
          >
            <Icon className='h-4 w-4' />
            {label}
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};

export default AdminSidebar;
