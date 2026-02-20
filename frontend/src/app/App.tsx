import { BrowserRouter } from 'react-router-dom';

import { QueryClient, QueryClientProvider } from '@tanstack/react-query';

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
        </SessionGuard>
      </QueryClientProvider>
    </BrowserRouter>
  );
};

export default App;
