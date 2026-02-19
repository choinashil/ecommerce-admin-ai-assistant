import { create } from 'zustand';

import { USERS } from '../lib/users';

import type { User } from './types';

interface UserStore {
  currentUser: User;
  switchUser: (user: User) => void;
}

export const useUserStore = create<UserStore>((set) => ({
  currentUser: USERS[0],
  switchUser: (user: User) => {
    set({ currentUser: user });
  },
}));
