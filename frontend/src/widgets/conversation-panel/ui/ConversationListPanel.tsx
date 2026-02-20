import { ErrorBoundary, Suspense } from '@suspensive/react';
import { SuspenseQuery } from '@suspensive/react-query';

import { ConversationTable, conversationQueries } from '@/entities/conversation';

const ConversationListPanel = () => {
  return (
    <div className='flex-1 overflow-auto rounded-t-2xl bg-background p-6 shadow-sm'>
      <h2 className='text-2xl font-bold'>LLM 로그</h2>
      <p className='mt-2text-muted-foreground'>대화 내역 및 LLM 호출 메타데이터</p>

      <div className='mt-6'>
        <ErrorBoundary
          fallback={({ error }) => <p className='text-destructive'>{error.message}</p>}
        >
          <Suspense fallback={<p className='text-muted-foreground'>로딩 중...</p>}>
            <SuspenseQuery {...conversationQueries.list()}>
              {({ data: conversations }) => <ConversationTable conversations={conversations} />}
            </SuspenseQuery>
          </Suspense>
        </ErrorBoundary>
      </div>
    </div>
  );
};

export default ConversationListPanel;
