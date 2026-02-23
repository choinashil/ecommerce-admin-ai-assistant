import { GUIDE_PROMPTS } from '../data/guide-prompts';
import {
  generateProductCreatePrompt,
  generateProductDeletePrompt,
  generateProductQueryPrompt,
  generateProductUpdatePrompt,
} from '../data/product-prompts';

import type { ProductInfo, PromptCategory } from '../model/types';

const MAX_RETRY_ATTEMPTS = 10;
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

const pickFromCategory = (category: PromptCategory, products: ProductInfo[]): string => {
  switch (category) {
    case 'guide': {
      const index = Math.floor(Math.random() * GUIDE_PROMPTS.length);
      return GUIDE_PROMPTS[index];
    }
    case 'product_create':
      return generateProductCreatePrompt();
    case 'product_query':
      return generateProductQueryPrompt(products);
    case 'product_update':
      return generateProductUpdatePrompt(products);
    case 'product_delete':
      return generateProductDeletePrompt(products);
  }
};

export const pickRandomPrompts = (
  count: number,
  categoryFilter?: PromptCategory,
  products: ProductInfo[] = [],
): string[] => {
  const results: string[] = [];
  const seen = new Set<string>();

  for (let i = 0; i < count; i++) {
    const category = categoryFilter ?? pickCategory();
    let prompt = pickFromCategory(category, products);

    let attempts = 0;
    while (seen.has(prompt) && attempts < MAX_RETRY_ATTEMPTS) {
      prompt = pickFromCategory(category, products);
      attempts++;
    }

    seen.add(prompt);
    results.push(prompt);
  }

  return results;
};
