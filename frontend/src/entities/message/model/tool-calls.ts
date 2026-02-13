import type { components } from '@/shared/api/schema';

export type ToolCallDetail = components['schemas']['ToolCallDetail'];

interface FaqResult {
  id: string;
  title: string;
  url: string;
  breadcrumb: string;
  similarity: number;
}

export interface SearchFaqToolCall {
  name: 'search_faq';
  arguments: { query: string };
  result: { results: FaqResult[]; total: number };
}

export const isSearchFaqToolCall = (toolCall: ToolCallDetail): toolCall is SearchFaqToolCall => {
  return toolCall.name === 'search_faq';
};
