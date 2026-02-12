import type { Message } from '@/entities/message';

export interface ChatState {
  messages: Message[];
  conversationId: string | null;
  isStreaming: boolean;
  error: string | null;
}

export type ChatAction =
  | { type: 'ADD_USER_MESSAGE'; payload: { id: string; content: string } }
  | { type: 'ADD_ASSISTANT_MESSAGE'; payload: { id: string } }
  | { type: 'APPEND_TOKEN'; payload: { token: string } }
  | { type: 'SET_CONVERSATION_ID'; payload: { id: string } }
  | { type: 'SET_STREAMING'; payload: { isStreaming: boolean } }
  | { type: 'SET_ERROR'; payload: { error: string | null } };
