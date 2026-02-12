import { useQuery } from '@tanstack/react-query';

import { ConversationTable, conversationQueries } from '@/entities/conversation';

const LogsPage = () => {
  const { data: conversations = [], isLoading, error } = useQuery(conversationQueries.list());

  return (
    <div className='p-6'>
      <h1 className='text-2xl font-bold'>LLM 로그</h1>
      <p className='mt-2 mb-6 text-muted-foreground'>대화 내역 및 LLM 호출 메타데이터</p>

      {isLoading && <p className='text-muted-foreground'>로딩 중...</p>}
      {error && <p className='text-destructive'>{error.message}</p>}
      {!isLoading && !error && <ConversationTable conversations={conversations} />}
    </div>
  );
};

export default LogsPage;
