import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';

import { initGA } from '@/shared/lib/analytics';

import './index.css';
import App from './App.tsx';

initGA();

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <App />
  </StrictMode>,
);
