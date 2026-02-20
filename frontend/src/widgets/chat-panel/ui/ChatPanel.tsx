import { useCallback, useRef, useState } from 'react';

import { Bot, SquarePen } from 'lucide-react';

import type { Message } from '@/entities/message';
import MessageList from '@/entities/message/ui/MessageList';
import { ChatHistoryPopover } from '@/features/chat-history';
import { useChat } from '@/features/send-message';
import MessageInput from '@/features/send-message/ui/MessageInput';
import { SuggestedPrompts } from '@/features/suggested-prompts';
import { Button } from '@/shared/ui/button';

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
    <aside className='flex w-100 flex-col overflow-hidden border-l bg-background'>
      <header className='flex items-center gap-2 border-b px-4 py-3'>
        <Bot className='h-5 w-5 text-primary' />
        <h2 className='font-semibold'>AI 어시스턴트</h2>
        <div className='ml-auto flex items-center gap-1'>
          <Button
            variant='ghost'
            size='icon'
            onClick={handleNewChat}
            disabled={isStreaming}
            aria-label='새 대화 시작'
          >
            <SquarePen className='size-4' />
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

      <MessageList messages={messages} statusMessage={statusMessage} />
      <SuggestedPrompts onSelect={handleSelectPrompt} isDisabled={isStreaming} />
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
