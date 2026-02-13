import { Bot } from 'lucide-react';

import MessageList from '@/entities/message/ui/MessageList';
import { useChat } from '@/features/send-message';
import MessageInput from '@/features/send-message/ui/MessageInput';

interface ChatPanelProps {
  onToolResult?: (toolName: string) => void;
}

const ChatPanel = ({ onToolResult }: ChatPanelProps) => {
  const { messages, isStreaming, error, sendMessage } = useChat({ onToolResult });

  return (
    <aside className='flex w-[400px] flex-col border-l bg-background'>
      <header className='flex items-center gap-2 border-b px-4 py-3'>
        <Bot className='h-5 w-5 text-primary' />
        <h2 className='font-semibold'>AI 어시스턴트</h2>
      </header>

      {error && (
        <div className='mx-4 mt-2 rounded-md bg-destructive/10 px-3 py-2 text-sm text-destructive'>
          {error}
        </div>
      )}

      <MessageList messages={messages} isStreaming={isStreaming} />
      <MessageInput onSend={sendMessage} isDisabled={isStreaming} />
    </aside>
  );
};

export default ChatPanel;
