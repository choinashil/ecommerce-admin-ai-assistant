import { queryOptions } from '@tanstack/react-query';

import { fetchConversations, fetchMyConversations } from './conversation.api';

export const conversationQueries = {
  all: () => ['conversations'] as const,
  lists: () => [...conversationQueries.all(), 'list'] as const,
  list: () =>
    queryOptions({
      queryKey: [...conversationQueries.lists()],
      queryFn: fetchConversations,
    }),
  myLists: () => [...conversationQueries.lists(), 'my'] as const,
  myList: () =>
    queryOptions({
      queryKey: [...conversationQueries.myLists()],
      queryFn: fetchMyConversations,
    }),
};
