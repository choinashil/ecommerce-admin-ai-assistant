import { ErrorBoundary, Suspense } from '@suspensive/react';
import { SuspenseQuery } from '@suspensive/react-query';
import { ArrowLeft } from 'lucide-react';

import { MessageTimeline, messageQueries } from '@/entities/message';

interface ConversationDetailPanelProps {
  id: string;
  onBack: () => void;
}

const ConversationDetailPanel = ({ id, onBack }: ConversationDetailPanelProps) => {
  return (
    <div className='flex-1 overflow-auto rounded-t-2xl bg-background p-6 shadow-sm'>
      <button
        className='mb-4 flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground'
        onClick={onBack}
      >
        <ArrowLeft className='h-4 w-4' />
        목록으로
      </button>
      <h2 className='text-2xl font-bold'>{id}</h2>

      <div className='mt-6'>
        <ErrorBoundary
          fallback={({ error }) => <p className='text-destructive'>{error.message}</p>}
        >
          <Suspense fallback={<p className='text-muted-foreground'>로딩 중...</p>}>
            <SuspenseQuery {...messageQueries.list(id)}>
              {({ data: messages }) => <MessageTimeline messages={messages} />}
            </SuspenseQuery>
          </Suspense>
        </ErrorBoundary>
      </div>
    </div>
  );
};

export default ConversationDetailPanel;
