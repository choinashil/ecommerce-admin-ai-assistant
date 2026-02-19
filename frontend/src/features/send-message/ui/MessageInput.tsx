import { useEffect, type KeyboardEvent, type RefObject } from 'react';

import { Send } from 'lucide-react';

import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';

interface MessageInputProps {
  value: string;
  onChange: (value: string) => void;
  onSend: (message: string) => void;
  isDisabled: boolean;
  inputRef: RefObject<HTMLInputElement | null>;
}

const MessageInput = ({ value, onChange, onSend, isDisabled, inputRef }: MessageInputProps) => {
  useEffect(() => {
    if (!isDisabled) {
      inputRef.current?.focus();
    }
  }, [isDisabled, inputRef]);

  const handleSubmit = (e: React.SyntheticEvent) => {
    e.preventDefault();
    const trimmed = value.trim();
    if (!trimmed || isDisabled) {
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
    <form onSubmit={handleSubmit} className='flex items-center gap-2 border-t px-4 py-3'>
      <Input
        ref={inputRef}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder='메시지를 입력하세요...'
        disabled={isDisabled}
        className='flex-1'
      />
      <Button type='submit' size='icon' disabled={isDisabled || !value.trim()}>
        <Send className='h-4 w-4' />
      </Button>
    </form>
  );
};

export default MessageInput;
