import { useEffect, useRef } from 'react';
import { Virtuoso, type VirtuosoHandle } from 'react-virtuoso';

import AssistantMessage from './AssistantMessage';
import StreamingStatus from './StreamingStatus';
import UserMessage from './UserMessage';

import type { Message } from '../model/types';

interface MessageListProps {
  messages: Message[];
  statusMessage?: string | null;
}

const MessageList = ({ messages, statusMessage }: MessageListProps) => {
  const virtuosoRef = useRef<VirtuosoHandle>(null);
  const scrollerRef = useRef<HTMLElement | null>(null);
  const isAtBottomRef = useRef(true);

  const lastMessage = messages[messages.length - 1];
  const isStreaming = lastMessage?.status === 'streaming';
  const isWaitingForResponse = isStreaming && lastMessage?.content === '';

  useEffect(() => {
    if (isAtBottomRef.current && scrollerRef.current) {
      const el = scrollerRef.current;
      el.scrollTop = el.scrollHeight;
    }
  });

  return (
    <Virtuoso
      key={messages[0]?.id ?? 'empty'}
      ref={virtuosoRef}
      scrollerRef={(ref) => {
        scrollerRef.current = ref as HTMLElement;
      }}
      data={messages}
      className='flex-1'
      atBottomStateChange={(atBottom) => {
        isAtBottomRef.current = atBottom;
      }}
      atBottomThreshold={100}
      initialTopMostItemIndex={messages.length - 1}
      itemContent={(_, message) => {
        if (message.status === 'streaming' && message.content === '') {
          return null;
        }

        return (
          <div className='px-4 pt-4'>
            {message.content &&
              (message.role === 'user' ? (
                <UserMessage content={message.content} />
              ) : (
                <AssistantMessage content={message.content} />
              ))}
            {message.status === 'aborted' && (
              <p className='text-center text-xs text-muted-foreground'>응답이 중단되었어요.</p>
            )}
          </div>
        );
      }}
      components={{
        Footer: () => {
          if (isWaitingForResponse && statusMessage) {
            return (
              <div className='px-4 pt-4 pb-10'>
                <StreamingStatus statusMessage={statusMessage} />
              </div>
            );
          }
          return <div className='h-10' />;
        },
      }}
    />
  );
};

export default MessageList;
