import MarkdownContent from '@/shared/ui/markdown-content';

interface AssistantMessageProps {
  content: string;
}

const AssistantMessage = ({ content }: AssistantMessageProps) => {
  return (
    <div className='min-w-0 text-sm'>
      <MarkdownContent content={content} />
    </div>
  );
};

export default AssistantMessage;
