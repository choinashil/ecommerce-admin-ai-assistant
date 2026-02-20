import { useEffect, useState } from 'react';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import { useSessionStore } from '@/entities/seller';
import { createSeller } from '@/features/create-seller';

import AppRoutes from './routes';

const queryClient = new QueryClient();

const App = () => {
  const { session, setSession } = useSessionStore();
  const [isReady, setIsReady] = useState(session !== null);

  useEffect(() => {
    if (session) {
      return;
    }

    createSeller().then((newSession) => {
      setSession(newSession);
      setIsReady(true);
    });
  }, [session, setSession]);

  if (!isReady) {
    return null;
  }

  return (
    <QueryClientProvider client={queryClient}>
      <AppRoutes />
    </QueryClientProvider>
  );
};

export default App;
