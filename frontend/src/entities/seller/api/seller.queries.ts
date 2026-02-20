import { queryOptions } from '@tanstack/react-query';

import { fetchSellerDetail } from './seller.api';

export const sellerQueries = {
  all: () => ['sellers'] as const,
  details: () => [...sellerQueries.all(), 'detail'] as const,
  detail: (id: string) =>
    queryOptions({
      queryKey: [...sellerQueries.details(), id],
      queryFn: () => fetchSellerDetail(id),
    }),
};
