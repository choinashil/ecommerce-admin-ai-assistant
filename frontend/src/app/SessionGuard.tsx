import { useEffect, useState } from 'react';

import { useSessionStore } from '@/entities/seller';
import { createSeller } from '@/features/create-seller';

const SessionGuard = ({ children }: { children: React.ReactNode }) => {
  const { session, setSession } = useSessionStore();
  const [isReady, setIsReady] = useState(session !== null);

  useEffect(() => {
    if (session) {
      return;
    }

    const init = async () => {
      try {
        const newSession = await createSeller();
        setSession(newSession);
      } catch (error) {
        console.error('판매자 세션 생성 실패:', error);
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
