import { formatRelativeTime } from '@/shared/lib/format';
import { cn } from '@/shared/lib/utils';

import type { ConversationSummary } from '../model/types';

interface ConversationItemProps {
  conversation: ConversationSummary;
  isActive: boolean;
  onClick: () => void;
}

const ConversationItem = ({ conversation, isActive, onClick }: ConversationItemProps) => {
  return (
    <button
      type='button'
      onClick={onClick}
      className={cn(
        'flex w-full flex-col gap-0.5 rounded-md px-1.5 py-1.5 text-left transition-colors',
        'hover:bg-accent/50',
        isActive && 'bg-accent',
      )}
    >
      <div className='flex items-center justify-between gap-2'>
        <span className='truncate text-xs font-medium'>
          {conversation.first_message || '새 대화'}
        </span>
        <span className='shrink-0 text-[0.625rem] text-muted-foreground'>
          {formatRelativeTime(conversation.updated_at)}
        </span>
      </div>
      <span className='text-[0.625rem] text-muted-foreground'>
        메시지 {conversation.message_count}개
      </span>
    </button>
  );
};

export default ConversationItem;
