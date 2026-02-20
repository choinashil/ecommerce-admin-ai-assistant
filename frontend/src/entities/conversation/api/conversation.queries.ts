import { queryOptions } from '@tanstack/react-query';

import { fetchConversations, fetchMyConversations } from './conversation.api';

export const conversationQueries = {
  all: () => ['conversations'] as const,
  lists: () => [...conversationQueries.all(), 'list'] as const,
  list: (sellerId?: string) =>
    queryOptions({
      queryKey: [...conversationQueries.lists(), { sellerId }],
      queryFn: () => fetchConversations(sellerId),
    }),
  myLists: () => [...conversationQueries.lists(), 'my'] as const,
  myList: () =>
    queryOptions({
      queryKey: [...conversationQueries.myLists()],
      queryFn: fetchMyConversations,
    }),
};
