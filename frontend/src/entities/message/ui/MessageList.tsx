import { useEffect, useRef, useState } from 'react';
import { Virtuoso, type VirtuosoHandle } from 'react-virtuoso';

import { ChevronDown } from 'lucide-react';

import { cn } from '@/shared/lib/utils';
import { Button } from '@/shared/ui/Button';

import AssistantMessage from './AssistantMessage';
import StreamingStatus from './StreamingStatus';
import UserMessage from './UserMessage';

import type { Message } from '../model/types';

const SCROLL_BOTTOM_THRESHOLD = 30;
const FOOTER_HEIGHT = 40;

interface MessageListProps {
  messages: Message[];
  statusMessage?: string | null;
}

const MessageList = ({ messages, statusMessage }: MessageListProps) => {
  const virtuosoRef = useRef<VirtuosoHandle>(null);
  const scrollerRef = useRef<HTMLElement | null>(null);
  const lastUserHeightRef = useRef(0);

  const [isAtBottom, setIsAtBottom] = useState(true);

  const lastMessage = messages[messages.length - 1];
  const isStreaming = lastMessage?.status === 'streaming';
  const isWaitingForResponse = isStreaming && lastMessage?.content === '';

  useEffect(() => {
    if (!isWaitingForResponse || messages.length < 2) {
      return;
    }

    // Virtuoso가 새 아이템(min-height 포함)을 렌더링/측정한 뒤 스크롤
    const timer = setTimeout(() => {
      virtuosoRef.current?.scrollToIndex({
        index: messages.length - 2,
        align: 'start',
      });
    }, 50);

    return () => clearTimeout(timer);
  }, [isWaitingForResponse, messages.length]);

  const handleScrollToBottom = () => {
    // atBottomStateChange로 setIsBottom 설정
    virtuosoRef.current?.scrollToIndex({
      index: messages.length - 1,
      behavior: 'smooth',
    });
  };

  return (
    <div className='relative flex-1 overflow-hidden'>
      <Virtuoso
        key={messages[0]?.id ?? 'empty'}
        ref={virtuosoRef}
        scrollerRef={(ref) => (scrollerRef.current = ref as HTMLElement)}
        data={messages}
        className='h-full'
        atBottomStateChange={setIsAtBottom}
        atBottomThreshold={SCROLL_BOTTOM_THRESHOLD}
        initialTopMostItemIndex={messages.length - 1}
        itemContent={(index, message) => {
          const isLastAssistantMessage = index === messages.length - 1;
          const isLastUserMessage = index === messages.length - 2;
          const assistantMinHeight =
            isLastAssistantMessage && scrollerRef.current?.clientHeight
              ? Math.max(
                  0,
                  scrollerRef.current.clientHeight - lastUserHeightRef.current - FOOTER_HEIGHT,
                )
              : undefined;

          // 응답 대기 중: min-height 공간 + StreamingStatus
          if (message.status === 'streaming' && message.content === '') {
            return (
              <div style={{ minHeight: assistantMinHeight }}>
                {statusMessage && (
                  <div className='px-4 pt-4'>
                    <StreamingStatus statusMessage={statusMessage} />
                  </div>
                )}
              </div>
            );
          }

          return (
            <div
              className='px-4 pt-4'
              ref={
                isLastUserMessage
                  ? (el) => {
                      if (el) {
                        lastUserHeightRef.current = el.offsetHeight;
                      }
                    }
                  : undefined
              }
            >
              {message.content &&
                (message.role === 'user' ? (
                  <UserMessage content={message.content} />
                ) : (
                  <AssistantMessage
                    content={message.content}
                    style={{ minHeight: assistantMinHeight }}
                  />
                ))}
              {message.status === 'aborted' && (
                <p className='text-center text-xs text-muted-foreground'>응답이 중단되었어요.</p>
              )}
            </div>
          );
        }}
        components={{
          Footer: () => <div style={{ height: FOOTER_HEIGHT }} />,
        }}
      />

      <div className='absolute right-4 bottom-2 z-10'>
        <Button
          variant='outline'
          size='icon'
          className={cn(
            'h-8 w-8 rounded-full bg-background shadow-md transition-opacity duration-200 hover:bg-accent',
            isAtBottom ? 'pointer-events-none opacity-0' : 'opacity-100',
          )}
          onClick={handleScrollToBottom}
          aria-label='맨 아래로 이동'
        >
          <ChevronDown className='h-4 w-4' />
        </Button>
      </div>
    </div>
  );
};

export default MessageList;
