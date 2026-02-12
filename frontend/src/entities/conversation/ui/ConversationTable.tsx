import { useNavigate } from 'react-router-dom';

import type { ConversationSummary } from '@/entities/conversation';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/shared/ui/table';

interface ConversationTableProps {
  conversations: ConversationSummary[];
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
};

const formatTokens = (tokens: number) => {
  return tokens.toLocaleString('ko-KR');
};

const ConversationTable = ({ conversations }: ConversationTableProps) => {
  const navigate = useNavigate();

  if (conversations.length === 0) {
    return <p className='text-muted-foreground'>대화 기록이 없습니다.</p>;
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>ID</TableHead>
          <TableHead>첫 메시지</TableHead>
          <TableHead className='text-right'>메시지 수</TableHead>
          <TableHead className='text-right'>총 토큰</TableHead>
          <TableHead>생성일시</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {conversations.map((conv) => (
          <TableRow
            key={conv.id}
            className='cursor-pointer'
            onClick={() => navigate(`/conversations/${conv.id}`)}
          >
            <TableCell className='font-mono'>{conv.id}</TableCell>
            <TableCell className='max-w-xs truncate'>{conv.first_message}</TableCell>
            <TableCell className='text-right'>{conv.message_count}</TableCell>
            <TableCell className='text-right'>{formatTokens(conv.total_tokens)}</TableCell>
            <TableCell className='text-muted-foreground'>{formatDate(conv.created_at)}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

export default ConversationTable;
