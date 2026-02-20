import { useNavigate, useParams } from 'react-router-dom';

import { ConversationDetailPanel } from '@/widgets/conversation-panel';

const ConversationDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  return <ConversationDetailPanel id={id!} onBack={() => navigate('/conversations')} />;
};

export default ConversationDetailPage;
