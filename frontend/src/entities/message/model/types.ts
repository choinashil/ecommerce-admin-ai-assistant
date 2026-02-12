import type { components } from '@/shared/api/schema';

export type MessageRole = 'user' | 'assistant';

export interface Message {
  id: string;
  role: MessageRole;
  content: string;
}

export type MessageMetadata = components['schemas']['MessageMetadata'];

export type MessageDetail = components['schemas']['MessageDetail'];
