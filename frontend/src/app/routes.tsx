import { Route, Routes } from 'react-router-dom';

import AdminPage from '@/pages/admin/AdminPage';
import ConversationDetailPage from '@/pages/conversations/ConversationDetailPage';
import ConversationsPage from '@/pages/conversations/ConversationsPage';

import DefaultLayout from './layouts/DefaultLayout';

const AppRoutes = () => {
  return (
    <Routes>
      <Route element={<DefaultLayout />}>
        <Route path='/' element={<AdminPage />} />
        <Route path='/conversations' element={<ConversationsPage />} />
        <Route path='/conversations/:id' element={<ConversationDetailPage />} />
      </Route>
    </Routes>
  );
};

export default AppRoutes;
