import { Shuffle } from 'lucide-react';

import { cn } from '@/shared/lib/utils';
import { Button } from '@/shared/ui/Button';

import { useRandomPrompts } from '../model/useRandomPrompts';

import type { PromptCategory } from '../model/types';

const PROMPT_COUNT = 3;

interface SuggestedPromptsProps {
  onSelect: (prompt: string) => void;
  isDisabled: boolean;
  variant?: 'centered' | 'inline';
  categoryFilter?: PromptCategory;
}

const SuggestedPrompts = ({
  onSelect,
  isDisabled,
  variant = 'inline',
  categoryFilter,
}: SuggestedPromptsProps) => {
  const { prompts, shuffle } = useRandomPrompts(PROMPT_COUNT, categoryFilter);
  const isCentered = variant === 'centered';

  return (
    <div
      className={cn(
        'flex flex-col gap-1',
        isCentered ? 'items-center text-muted-foreground' : 'px-4 py-2',
      )}
    >
      {!isCentered && (
        <div className='flex items-center'>
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
      )}
      <div className={cn('flex flex-col gap-1', isCentered && 'items-center')}>
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
      {isCentered && (
        <Button
          variant='ghost'
          size='sm'
          disabled={isDisabled}
          onClick={shuffle}
          className='text-xs text-muted-foreground'
        >
          <Shuffle className='h-3 w-3' />
          다른 프롬프트 보기
        </Button>
      )}
    </div>
  );
};

export default SuggestedPrompts;
