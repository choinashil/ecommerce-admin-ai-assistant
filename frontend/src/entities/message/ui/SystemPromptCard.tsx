import { ChevronDown, ChevronRight } from 'lucide-react';

import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/shared/ui/collapsible';

interface SystemPromptCardProps {
  prompt: string;
}

const SystemPromptCard = ({ prompt }: SystemPromptCardProps) => {
  return (
    <Collapsible>
      <div className='rounded-md border bg-muted/30 p-4'>
        <CollapsibleTrigger className='flex w-full items-center gap-2 text-left text-sm font-medium [&[data-state=closed]>svg:last-child]:hidden [&[data-state=open]>svg:first-child]:hidden'>
          <ChevronRight className='h-4 w-4' />
          <ChevronDown className='h-4 w-4' />
          시스템 프롬프트
        </CollapsibleTrigger>
        <CollapsibleContent>
          <p className='mt-3 text-sm whitespace-pre-wrap text-muted-foreground'>{prompt}</p>
        </CollapsibleContent>
      </div>
    </Collapsible>
  );
};

export default SystemPromptCard;
