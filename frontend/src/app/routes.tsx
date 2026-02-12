import { BrowserRouter, Route, Routes } from 'react-router-dom';

import AdminPage from '@/pages/admin/AdminPage';
import LogsPage from '@/pages/logs/LogsPage';

const AppRoutes = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path='/' element={<AdminPage />} />
        <Route path='/logs' element={<LogsPage />} />
      </Routes>
    </BrowserRouter>
  );
};

export default AppRoutes;
