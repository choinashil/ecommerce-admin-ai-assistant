import { useNavigate, useParams } from 'react-router-dom';

import { useQuery } from '@tanstack/react-query';
import { ArrowLeft } from 'lucide-react';

import { MessageTimeline, messageQueries } from '@/entities/message';

const ConversationDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: messages = [], isLoading, error } = useQuery(messageQueries.list(id!));

  return (
    <div className='flex-1 overflow-auto p-6'>
      <button
        className='mb-4 flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground'
        onClick={() => navigate('/conversations')}
      >
        <ArrowLeft className='h-4 w-4' />
        목록으로
      </button>

      <h1 className='mb-6 text-2xl font-bold'>{id}</h1>

      {isLoading && <p className='text-muted-foreground'>로딩 중...</p>}
      {error && <p className='text-destructive'>{error.message}</p>}
      {!isLoading && !error && <MessageTimeline messages={messages} />}
    </div>
  );
};

export default ConversationDetailPage;
