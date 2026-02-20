import { Navigate, useParams } from 'react-router-dom';

import { ROUTES } from '@/shared/config/routes';
import { useBackNavigation } from '@/shared/lib/useBackNavigation';
import { ConversationDetailPanel } from '@/widgets/conversation-panel';

const ConversationDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const { goBack } = useBackNavigation();

  if (!id) {
    return <Navigate to={ROUTES.CONVERSATIONS} replace />;
  }

  return <ConversationDetailPanel id={id} onBack={() => goBack(ROUTES.CONVERSATIONS)} />;
};

export default ConversationDetailPage;
