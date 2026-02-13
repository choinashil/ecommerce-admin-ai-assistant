import { useEffect, useRef, useState, type KeyboardEvent } from 'react';

import { Send } from 'lucide-react';

import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';

interface MessageInputProps {
  onSend: (message: string) => void;
  isDisabled: boolean;
}

const MessageInput = ({ onSend, isDisabled }: MessageInputProps) => {
  const inputRef = useRef<HTMLInputElement>(null);
  const [value, setValue] = useState('');

  useEffect(() => {
    if (!isDisabled) {
      inputRef.current?.focus();
    }
  }, [isDisabled]);

  const handleSubmit = (e: React.SyntheticEvent) => {
    e.preventDefault();
    const trimmed = value.trim();
    if (!trimmed || isDisabled) {
      return;
    }
    onSend(trimmed);
    setValue('');
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
        onChange={(e) => setValue(e.target.value)}
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
