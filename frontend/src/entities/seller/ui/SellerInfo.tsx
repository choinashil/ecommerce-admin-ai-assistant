import { Coins, Hash, MessageSquare } from 'lucide-react';

import { formatDate } from '@/shared/lib/format';
import StatCard from '@/shared/ui/StatCard';

import SellerInfoSkeleton from './SellerInfoSkeleton';

import type { SellerDetail } from '../model/types';

const SellerInfo = ({ seller }: { seller: SellerDetail }) => {
  return (
    <div>
      <h2 className='text-2xl font-bold'>{seller.nickname}</h2>
      <div className='mt-2 flex gap-4 text-sm text-muted-foreground'>
        <span>가입일: {formatDate(seller.created_at)}</span>
        {seller.last_active_at && <span>마지막 활동: {formatDate(seller.last_active_at)}</span>}
      </div>

      <div className='mt-6 grid grid-cols-3 gap-4'>
        <StatCard
          icon={<MessageSquare className='h-5 w-5' />}
          label='총 대화 수'
          value={seller.total_conversations}
        />
        <StatCard
          icon={<Hash className='h-5 w-5' />}
          label='총 메시지 수'
          value={seller.total_messages}
        />
        <StatCard
          icon={<Coins className='h-5 w-5' />}
          label='총 토큰 사용량'
          value={seller.total_tokens.toLocaleString('ko-KR')}
        />
      </div>
    </div>
  );
};

SellerInfo.Skeleton = SellerInfoSkeleton;

export default SellerInfo;
