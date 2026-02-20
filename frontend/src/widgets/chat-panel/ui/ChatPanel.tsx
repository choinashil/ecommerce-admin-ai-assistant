import { useCallback, useRef, useState } from 'react';

import { Bot, Plus } from 'lucide-react';

import type { Message } from '@/entities/message';
import MessageList from '@/entities/message/ui/MessageList';
import { ChatHistoryPopover } from '@/features/chat-history';
import { useChat } from '@/features/send-message';
import MessageInput from '@/features/send-message/ui/MessageInput';
import { SuggestedPrompts } from '@/features/suggested-prompts';
import { Button } from '@/shared/ui/Button';

interface ChatPanelProps {
  onToolResult?: (toolName: string) => void;
}

const ChatPanel = ({ onToolResult }: ChatPanelProps) => {
  const [inputValue, setInputValue] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSelectPrompt = (prompt: string) => {
    setInputValue(prompt);
    inputRef.current?.focus();
  };

  const {
    messages,
    isStreaming,
    statusMessage,
    error,
    conversationId,
    sendMessage,
    stopStreaming,
    loadConversation,
    resetChat,
  } = useChat({
    onToolResult,
    onAbort: setInputValue,
  });

  const handleSend = (message: string) => {
    sendMessage(message);
    setInputValue('');
  };

  const handleSelectConversation = useCallback(
    (selectedConversationId: string, selectedMessages: Message[]) => {
      loadConversation(selectedConversationId, selectedMessages);
      setInputValue('');
    },
    [loadConversation],
  );

  const handleNewChat = useCallback(() => {
    resetChat();
    setInputValue('');
  }, [resetChat]);

  return (
    <aside className='flex w-100 flex-col overflow-hidden rounded-t-2xl bg-background shadow-sm'>
      <header className='flex items-center gap-2 border-b px-4 py-3'>
        <Bot className='h-5 w-5 text-primary' />
        <h2 className='font-semibold'>AI 어시스턴트</h2>
        <div className='ml-auto flex items-center gap-1'>
          <Button variant='ghost' size='icon' onClick={handleNewChat} aria-label='새 대화 시작'>
            <Plus className='size-4' />
          </Button>
          <ChatHistoryPopover
            currentConversationId={conversationId}
            onSelectConversation={handleSelectConversation}
          />
        </div>
      </header>

      {error && (
        <div className='mx-4 mt-2 rounded-md bg-destructive/10 px-3 py-2 text-sm text-destructive'>
          {error}
        </div>
      )}

      {messages.length === 0 ? (
        <div className='flex flex-1 flex-col items-center justify-center gap-6 px-4'>
          <div className='flex flex-col items-center gap-1'>
            <p className='text-base font-medium text-foreground'>판매자님, 안녕하세요.</p>
            <p className='text-lg font-medium text-foreground'>무엇을 도와드릴까요?</p>
          </div>
          <SuggestedPrompts
            variant='centered'
            onSelect={handleSelectPrompt}
            isDisabled={isStreaming}
          />
        </div>
      ) : (
        <>
          <MessageList messages={messages} statusMessage={statusMessage} />
          <SuggestedPrompts onSelect={handleSelectPrompt} isDisabled={isStreaming} />
        </>
      )}
      <MessageInput
        value={inputValue}
        onChange={setInputValue}
        onSend={handleSend}
        onStop={stopStreaming}
        isStreaming={isStreaming}
        inputRef={inputRef}
      />
    </aside>
  );
};

export default ChatPanel;
