import { Skeleton } from '@/shared/ui/skeleton';

const MessageTimelineSkeleton = () => {
  return (
    <div className='flex flex-1 flex-col gap-4 p-4'>
      <div className='flex justify-end'>
        <Skeleton className='h-8 w-48 rounded-2xl' />
      </div>

      <div className='flex flex-col gap-2'>
        <Skeleton className='h-4 w-64' />
        <Skeleton className='h-4 w-52' />
        <Skeleton className='h-4 w-40' />
      </div>

      <div className='flex justify-end'>
        <Skeleton className='h-8 w-36 rounded-2xl' />
      </div>

      <div className='flex flex-col gap-2'>
        <Skeleton className='h-4 w-56' />
        <Skeleton className='h-4 w-44' />
      </div>
    </div>
  );
};

MessageTimelineSkeleton.displayName = 'MessageTimeline.Skeleton';

export default MessageTimelineSkeleton;
