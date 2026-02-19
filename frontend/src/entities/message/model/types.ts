import type { components } from '@/shared/api/schema';

export type MessageRole = 'user' | 'assistant';

export type MessageStatus = 'completed' | 'streaming' | 'aborted';

export interface Message {
  id: string;
  role: MessageRole;
  content: string;
  status: MessageStatus;
}

export type MessageMetadata = components['schemas']['MessageMetadata'];

export type MessageDetail = components['schemas']['MessageDetail'];
