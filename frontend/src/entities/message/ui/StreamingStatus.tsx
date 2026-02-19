import { Sparkles } from 'lucide-react';

interface StreamingStatusProps {
  statusMessage: string;
}

const StreamingStatus = ({ statusMessage }: StreamingStatusProps) => {
  return (
    <div className='flex items-center gap-2 py-2'>
      <Sparkles className='h-4 w-4 animate-pulse text-violet-500' strokeWidth={2} />
      <span className='animate-shimmer bg-linear-to-r from-violet-500 via-pink-500 to-violet-500 bg-size-[200%_100%] bg-clip-text text-sm font-medium text-transparent'>
        {statusMessage}
      </span>
    </div>
  );
};

export default StreamingStatus;
