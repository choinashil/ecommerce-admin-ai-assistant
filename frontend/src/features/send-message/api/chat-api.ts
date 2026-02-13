import type { components } from '@/shared/api/schema';
import { streamSSE } from '@/shared/api/sse-client';
import env from '@/shared/config/env';

export type ChatRequest = components['schemas']['ChatRequest'];

export interface ChatCallbacks {
  onConversationId: (id: string) => void;
  onContent: (token: string) => void;
  onToolResult?: (toolName: string) => void;
  onDone: () => void;
  onError: (error: Error) => void;
}

export const streamChat = async (request: ChatRequest, callbacks: ChatCallbacks): Promise<void> => {
  await streamSSE({
    url: `${env.API_BASE_URL}/api/chat`,
    body: request,
    onEvent: (event) => {
      switch (event.type) {
        case 'conversation_id':
          callbacks.onConversationId(event.data);
          break;
        case 'content':
          callbacks.onContent(event.data);
          break;
        case 'tool_result':
          callbacks.onToolResult?.(event.data);
          break;
        case 'error':
          callbacks.onError(new Error(event.data));
          break;
        case 'done':
          callbacks.onDone();
          break;
      }
    },
    onError: callbacks.onError,
  });
};
