import type { ComponentProps } from 'react';

import MarkdownContent from '@/shared/ui/MarkdownContent';

interface AssistantMessageProps extends ComponentProps<'div'> {
  content: string;
}

const AssistantMessage = ({ content, ...props }: AssistantMessageProps) => {
  return (
    <div className='min-w-0 text-sm' {...props}>
      <MarkdownContent content={content} />
    </div>
  );
};

export default AssistantMessage;
