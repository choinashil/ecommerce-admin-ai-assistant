import { useCallback, useEffect, useMemo, useState } from 'react';

import { useQuery } from '@tanstack/react-query';

import { productQueries } from '@/entities/product';

import { pickRandomPrompts } from '../lib/utils';

import type { ProductInfo, PromptCategory } from './types';

export const useRandomPrompts = (count: number = 3, categoryFilter?: PromptCategory) => {
  const { data: products } = useQuery(productQueries.list());
  const productInfos = useMemo<ProductInfo[]>(
    () => products?.map((p) => ({ name: p.name, status: p.status })) ?? [],
    [products],
  );

  const [prompts, setPrompts] = useState(() =>
    pickRandomPrompts(count, categoryFilter, productInfos),
  );

  useEffect(() => {
    setPrompts(pickRandomPrompts(count, categoryFilter, productInfos));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [count, categoryFilter]);

  const shuffle = useCallback(() => {
    setPrompts(pickRandomPrompts(count, categoryFilter, productInfos));
  }, [count, categoryFilter, productInfos]);

  return { prompts, shuffle };
};
