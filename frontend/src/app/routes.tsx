import { Route, Routes } from 'react-router-dom';

import AdminPage from '@/pages/admin/AdminPage';
import ConversationDetailPage from '@/pages/conversations/ConversationDetailPage';
import ConversationsPage from '@/pages/conversations/ConversationsPage';
import { ROUTES } from '@/shared/config/routes';

import DefaultLayout from './layouts/DefaultLayout';

const AppRoutes = () => {
  return (
    <Routes>
      <Route element={<DefaultLayout />}>
        <Route path={ROUTES.HOME} element={<AdminPage />} />
        <Route path={ROUTES.CONVERSATIONS} element={<ConversationsPage />} />
        <Route path={`${ROUTES.CONVERSATIONS}/:id`} element={<ConversationDetailPage />} />
      </Route>
    </Routes>
  );
};

export default AppRoutes;
