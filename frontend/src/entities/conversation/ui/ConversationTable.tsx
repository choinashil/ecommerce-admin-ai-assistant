import type { MouseEvent } from 'react';
import { useNavigate } from 'react-router-dom';

import type { ConversationSummary } from '@/entities/conversation';
import { ROUTES } from '@/shared/config/routes';
import { formatDate } from '@/shared/lib/format';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/shared/ui/Table';

import ConversationTableSkeleton from './ConversationTableSkeleton';

interface ConversationTableProps {
  conversations: ConversationSummary[];
  isSellerVisible?: boolean;
}

const formatTokens = (tokens: number) => {
  return tokens.toLocaleString('ko-KR');
};

const ConversationTable = ({ conversations, isSellerVisible = true }: ConversationTableProps) => {
  const navigate = useNavigate();

  const handleSellerClick = (e: MouseEvent, sellerId: string | null | undefined) => {
    if (!sellerId) {
      return;
    }
    e.stopPropagation();
    navigate(ROUTES.SELLER_DETAIL(sellerId));
  };

  if (conversations.length === 0) {
    return <p className='text-muted-foreground'>대화 기록이 없습니다.</p>;
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>ID</TableHead>
          {isSellerVisible && <TableHead>판매자</TableHead>}
          <TableHead className='w-1/3'>첫 메시지</TableHead>
          <TableHead>메시지 수</TableHead>
          <TableHead>총 토큰</TableHead>
          <TableHead>생성일시</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {conversations.map((conv) => (
          <TableRow
            key={conv.id}
            className='cursor-pointer'
            onClick={() => navigate(ROUTES.CONVERSATION_DETAIL(conv.id))}
          >
            <TableCell className='font-mono'>{conv.id}</TableCell>
            {isSellerVisible && (
              <TableCell
                className={conv.seller_id ? 'cursor-pointer text-primary hover:underline' : ''}
                onClick={(e) => handleSellerClick(e, conv.seller_id)}
              >
                {conv.seller_nickname ?? '-'}
              </TableCell>
            )}
            <TableCell>{conv.first_message}</TableCell>
            <TableCell className='tabular-nums'>{conv.message_count}</TableCell>
            <TableCell className='tabular-nums'>{formatTokens(conv.total_tokens)}</TableCell>
            <TableCell>{formatDate(conv.created_at)}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

ConversationTable.Skeleton = ConversationTableSkeleton;

export default ConversationTable;
