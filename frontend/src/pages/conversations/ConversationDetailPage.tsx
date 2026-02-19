import { useNavigate, useParams } from 'react-router-dom';

import { ErrorBoundary, Suspense } from '@suspensive/react';
import { SuspenseQuery } from '@suspensive/react-query';
import { ArrowLeft } from 'lucide-react';

import { MessageTimeline, messageQueries } from '@/entities/message';

const ConversationDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  return (
    <div className='flex-1 overflow-auto p-6'>
      <button
        className='mb-4 flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground'
        onClick={() => navigate('/conversations')}
      >
        <ArrowLeft className='h-4 w-4' />
        목록으로
      </button>

      <h2 className='mb-6 text-2xl font-bold'>{id}</h2>

      <ErrorBoundary fallback={({ error }) => <p className='text-destructive'>{error.message}</p>}>
        <Suspense fallback={<p className='text-muted-foreground'>로딩 중...</p>}>
          <SuspenseQuery {...messageQueries.list(id!)}>
            {({ data: messages }) => <MessageTimeline messages={messages} />}
          </SuspenseQuery>
        </Suspense>
      </ErrorBoundary>
    </div>
  );
};

export default ConversationDetailPage;
