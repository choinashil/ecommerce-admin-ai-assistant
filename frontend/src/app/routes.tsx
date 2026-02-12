import { BrowserRouter, Route, Routes } from 'react-router-dom';

import AdminPage from '@/pages/admin/AdminPage';
import LogsPage from '@/pages/logs/LogsPage';

export default function AppRoutes() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AdminPage />} />
        <Route path="/logs" element={<LogsPage />} />
      </Routes>
    </BrowserRouter>
  );
}
