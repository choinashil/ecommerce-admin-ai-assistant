import { BrowserRouter, Navigate, Outlet, Route, Routes } from 'react-router-dom';

import { DEFAULT_PATHS, useUserStore } from '@/entities/user';
import type { UserRole } from '@/entities/user';
import AdminPage from '@/pages/admin/AdminPage';
import ConversationDetailPage from '@/pages/conversations/ConversationDetailPage';
import ConversationsPage from '@/pages/conversations/ConversationsPage';

import DefaultLayout from './layouts/DefaultLayout';

const ProtectedRoute = ({ allowedRoles }: { allowedRoles: UserRole[] }) => {
  const role = useUserStore((state) => state.currentUser.role);

  if (!allowedRoles.includes(role)) {
    return <Navigate to={DEFAULT_PATHS[role]} replace />;
  }

  return <Outlet />;
};

const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<DefaultLayout />}>
          <Route element={<ProtectedRoute allowedRoles={['seller']} />}>
            <Route path='/' element={<AdminPage />} />
          </Route>
          <Route element={<ProtectedRoute allowedRoles={['admin']} />}>
            <Route path='/conversations' element={<ConversationsPage />} />
            <Route path='/conversations/:id' element={<ConversationDetailPage />} />
          </Route>
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default AppRoutes;
