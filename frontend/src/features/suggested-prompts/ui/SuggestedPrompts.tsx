import { Shuffle } from 'lucide-react';

import { Button } from '@/shared/ui/button';

import { useRandomPrompts } from '../model/useRandomPrompts';

const PROMPT_COUNT = 3;

interface SuggestedPromptsProps {
  onSelect: (prompt: string) => void;
  isDisabled: boolean;
}

const SuggestedPrompts = ({ onSelect, isDisabled }: SuggestedPromptsProps) => {
  const { prompts, shuffle } = useRandomPrompts(PROMPT_COUNT);

  return (
    <div className='flex flex-col gap-1 border-t px-4 py-2'>
      <div className='flex items-center gap-1'>
        <span className='text-[0.6875rem] text-muted-foreground'>추천 프롬프트</span>
        <Button
          variant='ghost'
          size='icon-xs'
          disabled={isDisabled}
          onClick={shuffle}
          aria-label='다른 추천 프롬프트 보기'
        >
          <Shuffle className='h-3 w-3' />
        </Button>
      </div>
      <div className='flex flex-col gap-1'>
        {prompts.map((prompt) => (
          <Button
            key={prompt}
            variant='outline'
            size='sm'
            disabled={isDisabled}
            onClick={() => onSelect(prompt)}
            className='h-auto w-fit justify-start py-1 text-left text-xs whitespace-normal'
          >
            {prompt}
          </Button>
        ))}
      </div>
    </div>
  );
};

export default SuggestedPrompts;
