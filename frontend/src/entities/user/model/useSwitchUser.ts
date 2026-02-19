import { useNavigate } from 'react-router-dom';

import { DEFAULT_PATHS } from '../lib/users';

import { useUserStore } from './store';

import type { User } from './types';

export const useSwitchUser = () => {
  const { currentUser, switchUser } = useUserStore();
  const navigate = useNavigate();

  const handleSwitch = (user: User) => {
    if (user.id === currentUser.id) {
      return;
    }
    switchUser(user);
    navigate(DEFAULT_PATHS[user.role]);
  };

  return { currentUser, switchUser: handleSwitch };
};
