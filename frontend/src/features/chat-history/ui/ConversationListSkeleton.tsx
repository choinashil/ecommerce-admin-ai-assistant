import { Skeleton } from '@/shared/ui/Skeleton';

const ConversationListSkeleton = () => {
  return (
    <div className='flex flex-col gap-0.5'>
      {Array.from({ length: 4 }).map((_, i) => (
        <div key={i} className='flex flex-col gap-1 rounded-md px-1.5 py-1.5'>
          <div className='flex items-center justify-between gap-2'>
            <Skeleton className='h-3 w-36' />
            <Skeleton className='h-2.5 w-10' />
          </div>
          <Skeleton className='h-2.5 w-16' />
        </div>
      ))}
    </div>
  );
};

ConversationListSkeleton.displayName = 'ConversationList.Skeleton';

export default ConversationListSkeleton;
