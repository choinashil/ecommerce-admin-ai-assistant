import { useEffect, useRef } from 'react';

import { ScrollArea } from '@/shared/ui/scroll-area';

import MessageItem from './MessageItem';
import TypingIndicator from './TypingIndicator';

import type { Message } from '../model/types';

interface MessageListProps {
  messages: Message[];
  isStreaming: boolean;
}

const MessageList = ({ messages, isStreaming }: MessageListProps) => {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const lastMessage = messages[messages.length - 1];
  const isWaitingForResponse = isStreaming && lastMessage?.content === '';
  const visibleMessages = isWaitingForResponse ? messages.slice(0, -1) : messages;

  return (
    <ScrollArea className='flex-1 overflow-hidden px-4'>
      <div className='flex flex-col gap-4 py-4'>
        {messages.length === 0 && (
          <div className='flex flex-col items-center justify-center py-12 text-center text-muted-foreground'>
            <p className='text-sm'>무엇이든 물어보세요!</p>
            <p className='mt-1 text-xs'>상품 등록, 매출 조회, 가이드 검색 등을 도와드립니다.</p>
          </div>
        )}
        {visibleMessages.map((message) => (
          <MessageItem key={message.id} message={message} />
        ))}
        {isWaitingForResponse && <TypingIndicator />}
        <div ref={bottomRef} />
      </div>
    </ScrollArea>
  );
};

export default MessageList;
