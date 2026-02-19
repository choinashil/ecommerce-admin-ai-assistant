import Markdown from 'react-markdown';

import { cn } from '@/shared/lib/utils';

interface MarkdownContentProps {
  content: string;
  className?: string;
}

const MarkdownContent = ({ content, className }: MarkdownContentProps) => {
  return (
    <div className={cn('prose prose-sm', className)}>
      <Markdown
        components={{
          a: ({ children, ...props }) => (
            <a target='_blank' rel='noopener noreferrer' {...props}>
              {children}
            </a>
          ),
        }}
      >
        {content}
      </Markdown>
    </div>
  );
};

export default MarkdownContent;
