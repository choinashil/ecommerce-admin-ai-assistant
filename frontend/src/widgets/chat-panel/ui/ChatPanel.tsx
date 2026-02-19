import { useRef, useState } from 'react';

import { Bot } from 'lucide-react';

import MessageList from '@/entities/message/ui/MessageList';
import { useChat } from '@/features/send-message';
import MessageInput from '@/features/send-message/ui/MessageInput';
import { SuggestedPrompts } from '@/features/suggested-prompts';

interface ChatPanelProps {
  onToolResult?: (toolName: string) => void;
}

const ChatPanel = ({ onToolResult }: ChatPanelProps) => {
  const { messages, isStreaming, statusMessage, error, sendMessage } = useChat({ onToolResult });
  const [inputValue, setInputValue] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSend = (message: string) => {
    sendMessage(message);
    setInputValue('');
  };

  const handleSelectPrompt = (prompt: string) => {
    setInputValue(prompt);
    inputRef.current?.focus();
  };

  return (
    <aside className='flex w-100 flex-col overflow-hidden border-l bg-background'>
      <header className='flex items-center gap-2 border-b px-4 py-3'>
        <Bot className='h-5 w-5 text-primary' />
        <h2 className='font-semibold'>AI 어시스턴트</h2>
      </header>

      {error && (
        <div className='mx-4 mt-2 rounded-md bg-destructive/10 px-3 py-2 text-sm text-destructive'>
          {error}
        </div>
      )}

      <MessageList messages={messages} isStreaming={isStreaming} statusMessage={statusMessage} />
      <SuggestedPrompts onSelect={handleSelectPrompt} isDisabled={isStreaming} />
      <MessageInput
        value={inputValue}
        onChange={setInputValue}
        onSend={handleSend}
        isDisabled={isStreaming}
        inputRef={inputRef}
      />
    </aside>
  );
};

export default ChatPanel;
