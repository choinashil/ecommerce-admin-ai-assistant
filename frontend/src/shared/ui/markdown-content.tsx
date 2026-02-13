import Markdown from 'react-markdown';

import { cn } from '@/shared/lib/utils';

interface MarkdownContentProps {
  content: string;
  className?: string;
}

const MarkdownContent = ({ content, className }: MarkdownContentProps) => {
  return (
    <div className={cn('prose prose-sm', className)}>
      <Markdown>{content}</Markdown>
    </div>
  );
};

export default MarkdownContent;
