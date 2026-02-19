import { Check, ChevronDown } from 'lucide-react';

import { USERS, useSwitchUser } from '@/entities/user';
import { cn } from '@/shared/lib/utils';
import { Avatar, AvatarFallback } from '@/shared/ui/avatar';
import { Popover, PopoverContent, PopoverTrigger } from '@/shared/ui/popover';

const ProfileMenu = () => {
  const { currentUser, switchUser } = useSwitchUser();

  return (
    <Popover>
      <PopoverTrigger asChild>
        <button className='flex items-center gap-2 rounded-md px-3 py-2 transition-colors hover:bg-muted'>
          <Avatar size='sm'>
            <AvatarFallback>{currentUser.name[0]}</AvatarFallback>
          </Avatar>
          <span className='text-sm font-medium'>{currentUser.name}</span>
          <ChevronDown className='h-3 w-3 text-muted-foreground' />
        </button>
      </PopoverTrigger>
      <PopoverContent align='end' className='w-52'>
        <div className='space-y-1'>
          {USERS.map((user) => {
            const isSelected = currentUser.id === user.id;
            return (
              <button
                key={user.id}
                onClick={() => switchUser(user)}
                className={cn(
                  'flex w-full items-center gap-3 rounded-md px-3 py-2 text-sm transition-colors',
                  isSelected ? 'bg-primary text-primary-foreground' : 'hover:bg-muted',
                )}
              >
                <Avatar size='sm'>
                  <AvatarFallback>{user.name[0]}</AvatarFallback>
                </Avatar>
                <span className='flex-1 text-left'>{user.name}</span>
                {isSelected && <Check className='h-4 w-4' />}
              </button>
            );
          })}
        </div>
      </PopoverContent>
    </Popover>
  );
};

export default ProfileMenu;
