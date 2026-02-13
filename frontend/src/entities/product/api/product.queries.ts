import { queryOptions } from '@tanstack/react-query';

import { fetchProducts } from './product.api';

export const productQueries = {
  all: () => ['products'] as const,
  lists: () => [...productQueries.all(), 'list'] as const,
  list: () =>
    queryOptions({
      queryKey: [...productQueries.lists()],
      queryFn: fetchProducts,
    }),
};
