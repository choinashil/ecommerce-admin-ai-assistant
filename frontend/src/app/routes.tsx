import { BrowserRouter, Route, Routes } from 'react-router-dom';

import AdminPage from '@/pages/admin/AdminPage';
import ConversationDetailPage from '@/pages/conversations/ConversationDetailPage';
import ConversationsPage from '@/pages/conversations/ConversationsPage';

import DefaultLayout from './layouts/DefaultLayout';

const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<DefaultLayout />}>
          <Route path='/' element={<AdminPage />} />
          <Route path='/conversations' element={<ConversationsPage />} />
          <Route path='/conversations/:id' element={<ConversationDetailPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default AppRoutes;
