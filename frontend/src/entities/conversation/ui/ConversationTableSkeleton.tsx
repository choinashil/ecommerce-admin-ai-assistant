import TableSkeleton from '@/shared/ui/TableSkeleton';

const ConversationTableSkeleton = () => {
  return <TableSkeleton columns={6} />;
};

ConversationTableSkeleton.displayName = 'ConversationTable.Skeleton';

export default ConversationTableSkeleton;
