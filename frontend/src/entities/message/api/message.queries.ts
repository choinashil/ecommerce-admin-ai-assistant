import { queryOptions } from '@tanstack/react-query';

import { fetchMessages, fetchMyMessages } from './message.api';

export const messageQueries = {
  all: () => ['messages'] as const,
  lists: () => [...messageQueries.all(), 'list'] as const,
  list: (conversationId: string) =>
    queryOptions({
      queryKey: [...messageQueries.lists(), conversationId],
      queryFn: () => fetchMessages(conversationId),
    }),
  myLists: () => [...messageQueries.lists(), 'my'] as const,
  myList: (conversationId: string) =>
    queryOptions({
      queryKey: [...messageQueries.myLists(), conversationId],
      queryFn: () => fetchMyMessages(conversationId),
    }),
};
