import { create } from 'zustand';
import { persist } from 'zustand/middleware';

import type { SellerSession } from './types';

interface SessionStore {
  session: SellerSession | null;
  setSession: (session: SellerSession) => void;
  clearSession: () => void;
}

export const useSessionStore = create<SessionStore>()(
  persist(
    (set) => ({
      session: null,
      setSession: (session) => set({ session }),
      clearSession: () => set({ session: null }),
    }),
    { name: 'seller-session' },
  ),
);
