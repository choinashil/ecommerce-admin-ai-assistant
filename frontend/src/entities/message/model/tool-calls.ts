import type { components } from '@/shared/api/schema';

export type ToolCallDetail = components['schemas']['ToolCallDetail'];

interface GuideResult {
  title: string;
  url: string;
  breadcrumb: string;
  similarity: number;
}

export interface SearchGuideToolCall {
  name: 'search_guide';
  arguments: { query: string };
  result: { results: GuideResult[]; total: number };
}

export const isSearchGuideToolCall = (toolCall: ToolCallDetail): toolCall is SearchGuideToolCall => {
  return toolCall.name === 'search_guide';
};
