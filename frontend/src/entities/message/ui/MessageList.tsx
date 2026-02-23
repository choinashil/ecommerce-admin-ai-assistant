import { useRef } from 'react';
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

  const lastMessage = messages[messages.length - 1];
  const isWaitingForResponse = lastMessage?.status === 'streaming' && lastMessage?.content === '';

  return (
    <Virtuoso
      key={messages[0]?.id ?? 'empty'}
      ref={virtuosoRef}
      data={messages}
      className='flex-1'
      followOutput='smooth'
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
              <div className='px-4 pt-4 pb-4'>
                <StreamingStatus statusMessage={statusMessage} />
              </div>
            );
          }
          return <div className='h-4' />;
        },
      }}
    />
  );
};

export default MessageList;
