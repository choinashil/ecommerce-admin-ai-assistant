import { useEffect, useRef, useState } from 'react';

import { useSessionStore } from '@/entities/seller';
import { createSeller } from '@/features/create-seller';

const SessionGuard = ({ children }: { children: React.ReactNode }) => {
  const { session, setSession } = useSessionStore();
  const [isReady, setIsReady] = useState(session !== null);
  const isInitializing = useRef(false);

  useEffect(() => {
    if (session || isInitializing.current) {
      return;
    }

    isInitializing.current = true;

    const init = async () => {
      try {
        const newSession = await createSeller();
        setSession(newSession);
      } catch (error) {
        console.error('판매자 세션 생성 실패:', error);
        isInitializing.current = false;
      } finally {
        setIsReady(true);
      }
    };

    init();
  }, [session, setSession]);

  if (!isReady) {
    return null;
  }

  return <>{children}</>;
};

export default SessionGuard;
