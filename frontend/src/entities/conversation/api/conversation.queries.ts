import { queryOptions } from '@tanstack/react-query';

import { fetchConversations } from './conversation.api';

export const conversationQueries = {
  all: () => ['conversations'] as const,
  lists: () => [...conversationQueries.all(), 'list'] as const,
  list: () =>
    queryOptions({
      queryKey: [...conversationQueries.lists()],
      queryFn: fetchConversations,
    }),
};
