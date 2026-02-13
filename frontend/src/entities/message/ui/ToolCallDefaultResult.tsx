import type { ToolCallDetail } from '../model/tool-calls';

interface ToolCallDefaultResultProps {
  toolCall: ToolCallDetail;
}

const ToolCallDefaultResult = ({ toolCall }: ToolCallDefaultResultProps) => {
  return (
    <div className='space-y-1.5'>
      <div>
        <span className='font-medium text-muted-foreground'>Arguments</span>
        <pre className='mt-0.5 overflow-auto rounded bg-muted p-1.5'>
          {JSON.stringify(toolCall.arguments, null, 2)}
        </pre>
      </div>
      <div>
        <span className='font-medium text-muted-foreground'>Result</span>
        <pre className='mt-0.5 overflow-auto rounded bg-muted p-1.5'>
          {JSON.stringify(toolCall.result, null, 2)}
        </pre>
      </div>
    </div>
  );
};

export default ToolCallDefaultResult;
