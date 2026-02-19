import { useEffect } from 'react';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import { useUserStore } from '@/entities/user';
import { applyTheme } from '@/shared/lib/theme';

import AppRoutes from './routes';

const queryClient = new QueryClient();

const App = () => {
  const role = useUserStore((state) => state.currentUser.role);

  useEffect(() => {
    applyTheme(role);
  }, [role]);

  return (
    <QueryClientProvider client={queryClient}>
      <AppRoutes />
    </QueryClientProvider>
  );
};

export default App;
