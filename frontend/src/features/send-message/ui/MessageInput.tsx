import { useEffect, type KeyboardEvent, type RefObject } from 'react';

import { Send, Square } from 'lucide-react';

import { Button } from '@/shared/ui/Button';
import { Input } from '@/shared/ui/Input';

interface MessageInputProps {
  value: string;
  onChange: (value: string) => void;
  onSend: (message: string) => void;
  onStop: () => void;
  isStreaming: boolean;
  inputRef: RefObject<HTMLInputElement | null>;
}

const MessageInput = ({
  value,
  onChange,
  onSend,
  onStop,
  isStreaming,
  inputRef,
}: MessageInputProps) => {
  useEffect(() => {
    if (!isStreaming) {
      inputRef.current?.focus();
    }
  }, [isStreaming, inputRef]);

  const handleSubmit = (e: React.SyntheticEvent) => {
    e.preventDefault();
    const trimmed = value.trim();
    if (!trimmed || isStreaming) {
      return;
    }
    onSend(trimmed);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className='px-4 py-3'>
      <div className='flex items-center gap-1 rounded-md border border-input bg-input/20 px-2 focus-within:border-ring/50'>
        <Input
          ref={inputRef}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder='메시지를 입력하세요...'
          disabled={isStreaming}
          className='h-10 flex-1 border-0 bg-transparent focus-visible:ring-0 md:text-sm'
        />
        {isStreaming ? (
          <Button key='stop' type='button' size='icon' variant='destructive' onClick={onStop}>
            <Square className='h-3 w-3' />
          </Button>
        ) : (
          <Button key='send' type='submit' size='icon' variant='ghost' disabled={!value.trim()}>
            <Send className='h-4 w-4' />
          </Button>
        )}
      </div>
    </form>
  );
};

export default MessageInput;
