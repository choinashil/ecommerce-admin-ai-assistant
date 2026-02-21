import { useState } from 'react';

import { ErrorBoundary, Suspense } from '@suspensive/react';
import { SuspenseQuery } from '@suspensive/react-query-5';
import { useQueryClient } from '@tanstack/react-query';
import { History } from 'lucide-react';

import { conversationQueries } from '@/entities/conversation';
import type { Message } from '@/entities/message';
import { convertToMessages, messageQueries } from '@/entities/message';
import { Button } from '@/shared/ui/Button';
import {
  Popover,
  PopoverContent,
  PopoverHeader,
  PopoverTitle,
  PopoverTrigger,
} from '@/shared/ui/Popover';
import { ScrollArea } from '@/shared/ui/ScrollArea';

import ConversationList from './ConversationList';

interface ChatHistoryPopoverProps {
  currentConversationId: string | null;
  onSelectConversation: (conversationId: string, messages: Message[]) => void;
}

const ChatHistoryPopover = ({
  currentConversationId,
  onSelectConversation,
}: ChatHistoryPopoverProps) => {
  const [isOpen, setIsOpen] = useState(false);
  const queryClient = useQueryClient();

  const handleOpenChange = (open: boolean) => {
    setIsOpen(open);

    if (open) {
      queryClient.invalidateQueries({ queryKey: conversationQueries.myLists() });
    }
  };

  const handleSelectConversation = async (conversationId: string) => {
    const details = await queryClient.fetchQuery(messageQueries.myList(conversationId));
    const messages = convertToMessages(details);
    onSelectConversation(conversationId, messages);
    setIsOpen(false);
  };

  return (
    <Popover open={isOpen} onOpenChange={handleOpenChange}>
      <PopoverTrigger asChild>
        <Button variant='ghost' size='icon' aria-label='대화 기록'>
          <History className='size-4' />
        </Button>
      </PopoverTrigger>
      <PopoverContent side='bottom' align='end' className='w-72 gap-2 p-1.5'>
        <PopoverHeader className='px-1.5 pt-0.5'>
          <PopoverTitle>대화 기록</PopoverTitle>
        </PopoverHeader>
        <ScrollArea className='max-h-80'>
          <ErrorBoundary
            fallback={({ error }) => (
              <p className='py-4 text-center text-destructive'>{error.message}</p>
            )}
          >
            <Suspense fallback={<ConversationList.Skeleton />}>
              <SuspenseQuery {...conversationQueries.myList()}>
                {({ data: conversations }) => (
                  <ConversationList
                    conversations={conversations}
                    currentConversationId={currentConversationId}
                    onSelectConversation={handleSelectConversation}
                  />
                )}
              </SuspenseQuery>
            </Suspense>
          </ErrorBoundary>
        </ScrollArea>
      </PopoverContent>
    </Popover>
  );
};

export default ChatHistoryPopover;
