import { Navigate, useParams } from 'react-router-dom';

import { useBackNavigation } from '@/shared/lib/useBackNavigation';
import { ConversationDetailPanel } from '@/widgets/conversation-panel';

const ConversationDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const { goBack } = useBackNavigation();

  if (!id) {
    return <Navigate to="/conversations" replace />;
  }

  return <ConversationDetailPanel id={id} onBack={() => goBack('/conversations')} />;
};

export default ConversationDetailPage;
