import { BrowserRouter, Route, Routes } from 'react-router-dom';

import AdminPage from '@/pages/admin/AdminPage';
import ConversationDetailPage from '@/pages/conversations/ConversationDetailPage';
import ConversationsPage from '@/pages/conversations/ConversationsPage';

const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<AdminPage />} />
        <Route path='/conversations' element={<ConversationsPage />} />
        <Route path='/conversations/:id' element={<ConversationDetailPage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRoutes;
