import { BrowserRouter } from 'react-router-dom';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

import { OnboardingGuide } from '@/features/onboarding';

import AppRoutes from './routes';
import SessionGuard from './SessionGuard';
import ThemeSync from './ThemeSync';

const queryClient = new QueryClient();

const App = () => {
  return (
    <BrowserRouter>
      <QueryClientProvider client={queryClient}>
        <ThemeSync />
        <SessionGuard>
          <AppRoutes />
          <OnboardingGuide />
        </SessionGuard>
      </QueryClientProvider>
    </BrowserRouter>
  );
};

export default App;
