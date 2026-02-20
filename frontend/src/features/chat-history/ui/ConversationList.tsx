import { ConversationItem } from '@/entities/conversation';
import type { ConversationSummary } from '@/entities/conversation';

interface ConversationListProps {
  conversations: ConversationSummary[];
  currentConversationId: string | null;
  onSelectConversation: (conversationId: string) => void;
}

const ConversationList = ({
  conversations,
  currentConversationId,
  onSelectConversation,
}: ConversationListProps) => {
  if (conversations.length === 0) {
    return <p className='py-4 text-center text-muted-foreground'>아직 대화가 없어요</p>;
  }

  return (
    <div className='flex flex-col gap-0.5'>
      {conversations.map((conversation) => (
        <ConversationItem
          key={conversation.id}
          conversation={conversation}
          isActive={conversation.id === currentConversationId}
          onClick={() => onSelectConversation(conversation.id)}
        />
      ))}
    </div>
  );
};

export default ConversationList;
