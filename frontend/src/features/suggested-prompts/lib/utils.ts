import { GUIDE_PROMPTS } from '../data/guide-prompts';
import {
  generateProductCreatePrompt,
  generateProductDeletePrompt,
  generateProductUpdatePrompt,
  PRODUCT_QUERY_PROMPTS,
} from '../data/product-prompts';

import type { PromptCategory } from '../model/types';

const WEIGHTED_CATEGORIES: { category: PromptCategory; weight: number }[] = [
  { category: 'guide', weight: 3 },
  { category: 'product_create', weight: 1 },
  { category: 'product_query', weight: 1 },
  { category: 'product_update', weight: 1 },
  { category: 'product_delete', weight: 1 },
];

const totalWeight = WEIGHTED_CATEGORIES.reduce((sum, c) => sum + c.weight, 0);

const pickCategory = (): PromptCategory => {
  let random = Math.random() * totalWeight;
  for (const { category, weight } of WEIGHTED_CATEGORIES) {
    random -= weight;
    if (random <= 0) {
      return category;
    }
  }
  return WEIGHTED_CATEGORIES[0].category;
};

const pickFromCategory = (category: PromptCategory): string => {
  switch (category) {
    case 'guide': {
      const index = Math.floor(Math.random() * GUIDE_PROMPTS.length);
      return GUIDE_PROMPTS[index];
    }
    case 'product_create':
      return generateProductCreatePrompt();
    case 'product_query': {
      const index = Math.floor(Math.random() * PRODUCT_QUERY_PROMPTS.length);
      return PRODUCT_QUERY_PROMPTS[index];
    }
    case 'product_update':
      return generateProductUpdatePrompt();
    case 'product_delete':
      return generateProductDeletePrompt();
  }
};

export const pickRandomPrompts = (count: number, categoryFilter?: PromptCategory): string[] => {
  const results: string[] = [];
  const seen = new Set<string>();

  for (let i = 0; i < count; i++) {
    const category = categoryFilter ?? pickCategory();
    let prompt = pickFromCategory(category);

    // 중복 방지: 같은 프롬프트가 나오면 재추출 (최대 10회)
    let attempts = 0;
    while (seen.has(prompt) && attempts < 10) {
      prompt = pickFromCategory(category);
      attempts++;
    }

    seen.add(prompt);
    results.push(prompt);
  }

  return results;
};
