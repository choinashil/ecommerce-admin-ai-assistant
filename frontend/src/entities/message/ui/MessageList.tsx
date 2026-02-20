import { Fragment, useEffect, useRef } from 'react';

import { ScrollArea } from '@/shared/ui/ScrollArea';

import AssistantMessage from './AssistantMessage';
import StreamingStatus from './StreamingStatus';
import UserMessage from './UserMessage';

import type { Message } from '../model/types';

interface MessageListProps {
  messages: Message[];
  statusMessage?: string | null;
}

const MessageList = ({ messages, statusMessage }: MessageListProps) => {
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const lastMessage = messages[messages.length - 1];
  const isWaitingForResponse = lastMessage?.status === 'streaming' && lastMessage?.content === '';

  return (
    <ScrollArea className='flex-1 overflow-hidden px-4'>
      <div className='flex flex-col gap-4 py-4'>
        {messages.map((message) => (
          <Fragment key={message.id}>
            {message.status === 'streaming' && message.content === '' ? null : (
              <>
                {message.content &&
                  (message.role === 'user' ? (
                    <UserMessage content={message.content} />
                  ) : (
                    <AssistantMessage content={message.content} />
                  ))}
                {message.status === 'aborted' && (
                  <p className='text-center text-xs text-muted-foreground'>응답이 중단되었어요.</p>
                )}
              </>
            )}
          </Fragment>
        ))}
        {isWaitingForResponse && statusMessage && <StreamingStatus statusMessage={statusMessage} />}
        <div ref={bottomRef} />
      </div>
    </ScrollArea>
  );
};

export default MessageList;
