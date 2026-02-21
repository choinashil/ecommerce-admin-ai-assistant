import { useEffect, type KeyboardEvent, type RefObject } from 'react';

import { Send, Square } from 'lucide-react';

import { Button } from '@/shared/ui/Button';

interface MessageInputProps {
  value: string;
  onChange: (value: string) => void;
  onSend: (message: string) => void;
  onStop: () => void;
  isStreaming: boolean;
  inputRef: RefObject<HTMLTextAreaElement | null>;
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

  useEffect(() => {
    const el = inputRef.current;
    if (el) {
      el.style.height = 'auto';
      el.style.height = `${el.scrollHeight}px`;
    }
  }, [value, inputRef]);

  const handleSubmit = (e: React.SyntheticEvent) => {
    e.preventDefault();
    const trimmed = value.trim();
    if (!trimmed || isStreaming) {
      return;
    }
    onSend(trimmed);
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className='px-4 py-3'>
      <div className='flex items-end gap-1 rounded-md border border-input bg-input/20 px-2 focus-within:border-ring/50'>
        <textarea
          ref={inputRef}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder='메시지를 입력하세요...'
          disabled={isStreaming}
          rows={1}
          className='max-h-32 flex-1 resize-none bg-transparent py-2.5 text-sm leading-normal outline-none placeholder:text-muted-foreground disabled:cursor-not-allowed disabled:opacity-50 md:text-sm'
        />
        {isStreaming ? (
          <Button key='stop' type='button' size='icon' variant='ghost' onClick={onStop} className='mb-1.5 text-destructive hover:text-destructive'>
            <Square className='h-3 w-3' />
          </Button>
        ) : (
          <Button key='send' type='submit' size='icon' variant='ghost' disabled={!value.trim()} className='mb-1.5'>
            <Send className='h-4 w-4' />
          </Button>
        )}
      </div>
    </form>
  );
};

export default MessageInput;
