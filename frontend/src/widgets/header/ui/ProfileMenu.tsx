import { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

import { Check, ChevronDown, Settings, User } from 'lucide-react';

import { useSessionStore } from '@/entities/seller';
import { isAdminPath, ROUTES } from '@/shared/config/routes';
import { cn } from '@/shared/lib/utils';
import { Avatar, AvatarFallback } from '@/shared/ui/avatar';
import { Popover, PopoverContent, PopoverTrigger } from '@/shared/ui/popover';

const ProfileMenu = () => {
  const nickname = useSessionStore((state) => state.session?.nickname) ?? '';
  const navigate = useNavigate();
  const { pathname } = useLocation();
  const [isOpen, setIsOpen] = useState(false);

  const isAdmin = isAdminPath(pathname);

  const handleNavigate = (path: string) => {
    navigate(path);
    setIsOpen(false);
  };

  return (
    <Popover open={isOpen} onOpenChange={setIsOpen}>
      <PopoverTrigger asChild>
        <button className='flex items-center gap-2 rounded-md px-3 py-2 transition-colors hover:bg-muted'>
          <Avatar size='sm'>
            <AvatarFallback>
              {isAdmin ? <Settings className='h-3.5 w-3.5' /> : <User className='h-3.5 w-3.5' />}
            </AvatarFallback>
          </Avatar>
          <span className='text-sm font-medium'>{isAdmin ? '관리자' : nickname}</span>
          <ChevronDown className='h-3 w-3 text-muted-foreground' />
        </button>
      </PopoverTrigger>
      <PopoverContent align='end' className='w-auto gap-0'>
        <div className='space-y-1'>
          <button
            onClick={() => handleNavigate(ROUTES.HOME)}
            className={cn(
              'flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors',
              !isAdmin ? 'bg-primary text-primary-foreground' : 'hover:bg-muted',
            )}
          >
            <Avatar size='sm'>
              <AvatarFallback>
                <User className='h-3.5 w-3.5' />
              </AvatarFallback>
            </Avatar>
            <span className='flex-1 whitespace-nowrap text-left'>판매자 ({nickname})</span>
            {!isAdmin && <Check className='h-4 w-4' />}
          </button>
          <button
            onClick={() => handleNavigate(ROUTES.CONVERSATIONS)}
            className={cn(
              'flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors',
              isAdmin ? 'bg-primary text-primary-foreground' : 'hover:bg-muted',
            )}
          >
            <Avatar size='sm'>
              <AvatarFallback>
                <Settings className='h-3.5 w-3.5' />
              </AvatarFallback>
            </Avatar>
            <span className='flex-1 whitespace-nowrap text-left'>관리자</span>
            {isAdmin && <Check className='h-4 w-4' />}
          </button>
        </div>
      </PopoverContent>
    </Popover>
  );
};

export default ProfileMenu;
