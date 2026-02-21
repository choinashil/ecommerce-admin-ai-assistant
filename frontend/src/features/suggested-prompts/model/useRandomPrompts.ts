import { useCallback, useEffect, useState } from 'react';

import { pickRandomPrompts } from '../lib/utils';

import type { PromptCategory } from './types';

export const useRandomPrompts = (count: number = 3, categoryFilter?: PromptCategory) => {
  const [prompts, setPrompts] = useState(() => pickRandomPrompts(count, categoryFilter));

  useEffect(() => {
    setPrompts(pickRandomPrompts(count, categoryFilter));
  }, [count, categoryFilter]);

  const shuffle = useCallback(() => {
    setPrompts(pickRandomPrompts(count, categoryFilter));
  }, [count, categoryFilter]);

  return { prompts, shuffle };
};
