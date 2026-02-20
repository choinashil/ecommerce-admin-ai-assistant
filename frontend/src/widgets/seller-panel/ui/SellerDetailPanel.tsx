import { ErrorBoundary, Suspense } from '@suspensive/react';
import { SuspenseQuery } from '@suspensive/react-query';
import { ArrowLeft } from 'lucide-react';

import { ConversationTable, conversationQueries } from '@/entities/conversation';
import { SellerInfo, sellerQueries } from '@/entities/seller';

interface SellerDetailPanelProps {
  id: string;
  onBack: () => void;
}

const SellerDetailPanel = ({ id, onBack }: SellerDetailPanelProps) => {
  return (
    <div className='flex-1 overflow-auto rounded-t-2xl bg-background p-6 shadow-sm'>
      <button
        className='mb-4 flex items-center gap-1 text-sm text-muted-foreground hover:text-foreground'
        onClick={onBack}
      >
        <ArrowLeft className='h-4 w-4' />
        목록으로
      </button>

      <ErrorBoundary fallback={({ error }) => <p className='text-destructive'>{error.message}</p>}>
        <Suspense fallback={<SellerInfo.Skeleton />}>
          <SuspenseQuery {...sellerQueries.detail(id)}>
            {({ data: seller }) => <SellerInfo seller={seller} />}
          </SuspenseQuery>
        </Suspense>

        <div className='mt-8'>
          <h3 className='mb-4 text-lg font-semibold'>대화 목록</h3>
          <Suspense fallback={<ConversationTable.Skeleton />}>
            <SuspenseQuery {...conversationQueries.list(id)}>
              {({ data: conversations }) => (
                <ConversationTable conversations={conversations} isSellerVisible={false} />
              )}
            </SuspenseQuery>
          </Suspense>
        </div>
      </ErrorBoundary>
    </div>
  );
};

export default SellerDetailPanel;
