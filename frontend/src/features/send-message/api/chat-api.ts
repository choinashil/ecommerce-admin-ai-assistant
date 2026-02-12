import { streamSSE } from '@/shared/api/sse-client';
import env from '@/shared/config/env';

export interface ChatRequest {
  conversation_id?: number;
  message: string;
}

export interface ChatCallbacks {
  onConversationId: (id: number) => void;
  onContent: (token: string) => void;
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
          callbacks.onConversationId(Number(event.data));
          break;
        case 'content':
          callbacks.onContent(event.data);
          break;
        case 'done':
          callbacks.onDone();
          break;
      }
    },
    onError: callbacks.onError,
  });
};
