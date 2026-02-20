import { useSessionStore } from './store';

export const getToken = (): string | null => {
  return useSessionStore.getState().session?.token ?? null;
};
