import { Skeleton } from '@/shared/ui/Skeleton';

const SellerInfoSkeleton = () => {
  return (
    <div>
      <Skeleton className='h-8 w-48' />
      <div className='mt-1 flex gap-4'>
        <Skeleton className='h-5 w-40' />
        <Skeleton className='h-5 w-40' />
      </div>
      <div className='mt-6 grid grid-cols-3 gap-4'>
        {Array.from({ length: 3 }).map((_, i) => (
          <Skeleton key={i} className='h-20 rounded-lg' />
        ))}
      </div>
    </div>
  );
};

SellerInfoSkeleton.displayName = 'SellerInfo.Skeleton';

export default SellerInfoSkeleton;
