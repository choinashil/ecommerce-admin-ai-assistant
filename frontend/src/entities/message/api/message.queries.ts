import { queryOptions } from '@tanstack/react-query';

import { fetchMessages } from './message.api';

export const messageQueries = {
  all: () => ['messages'] as const,
  lists: () => [...messageQueries.all(), 'list'] as const,
  list: (conversationId: string) =>
    queryOptions({
      queryKey: [...messageQueries.lists(), conversationId],
      queryFn: () => fetchMessages(conversationId),
    }),
};
