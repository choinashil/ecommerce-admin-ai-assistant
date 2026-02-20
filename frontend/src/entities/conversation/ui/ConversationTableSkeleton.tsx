import TableSkeleton from '@/shared/ui/table-skeleton';

const ConversationTableSkeleton = () => {
  return <TableSkeleton columns={6} />;
};

ConversationTableSkeleton.displayName = 'ConversationTable.Skeleton';

export default ConversationTableSkeleton;
