import { useCallback, useReducer, useRef } from 'react';

import { streamChat } from '../api/chat-api';

import type { ChatAction, ChatState } from './types';

interface UseChatOptions {
  onToolResult?: (toolName: string) => void;
  onAbort?: (lastUserMessage: string) => void;
}

const PHASE_STATUS = {
  THINKING: '생각 중...',
  DEFAULT: '처리 중...',
} as const;

const TOOL_STATUS_MAP: Record<string, string> = {
  search_guide: '가이드 검색 중...',
  create_product: '상품 등록 중...',
  list_products: '상품 목록 조회 중...',
};

const initialState: ChatState = {
  messages: [],
  conversationId: null,
  isStreaming: false,
  statusMessage: null,
  error: null,
};

const chatReducer = (state: ChatState, action: ChatAction): ChatState => {
  switch (action.type) {
    case 'ADD_USER_MESSAGE':
      return {
        ...state,
        messages: [
          ...state.messages,
          {
            id: action.payload.id,
            role: 'user',
            content: action.payload.content,
            status: 'completed',
          },
        ],
      };

    case 'ADD_ASSISTANT_MESSAGE':
      return {
        ...state,
        messages: [
          ...state.messages,
          {
            id: action.payload.id,
            role: 'assistant',
            content: '',
            status: 'streaming',
          },
        ],
      };

    case 'APPEND_TOKEN': {
      const messages = [...state.messages];
      const lastMessage = messages[messages.length - 1];
      if (lastMessage && lastMessage.role === 'assistant') {
        messages[messages.length - 1] = {
          ...lastMessage,
          content: lastMessage.content + action.payload.token,
        };
      }
      return { ...state, messages };
    }

    case 'SET_MESSAGE_STATUS': {
      const messages = [...state.messages];
      const lastMessage = messages[messages.length - 1];
      if (lastMessage && lastMessage.role === 'assistant') {
        messages[messages.length - 1] = {
          ...lastMessage,
          status: action.payload.status,
        };
      }
      return { ...state, messages };
    }

    case 'SET_CONVERSATION_ID':
      return { ...state, conversationId: action.payload.id };

    case 'SET_STREAMING':
      return { ...state, isStreaming: action.payload.isStreaming };

    case 'SET_STATUS':
      return { ...state, statusMessage: action.payload.statusMessage };

    case 'SET_ERROR':
      return { ...state, error: action.payload.error };

    default:
      return state;
  }
};

export const useChat = (options?: UseChatOptions) => {
  const [state, dispatch] = useReducer(chatReducer, initialState);
  const abortControllerRef = useRef<AbortController | null>(null);

  const sendMessage = useCallback(
    async (content: string) => {
      const userMsgId = crypto.randomUUID();
      dispatch({
        type: 'ADD_USER_MESSAGE',
        payload: { id: userMsgId, content },
      });

      dispatch({ type: 'SET_STREAMING', payload: { isStreaming: true } });
      dispatch({ type: 'SET_STATUS', payload: { statusMessage: PHASE_STATUS.THINKING } });
      dispatch({ type: 'SET_ERROR', payload: { error: null } });

      const assistantMsgId = crypto.randomUUID();
      dispatch({
        type: 'ADD_ASSISTANT_MESSAGE',
        payload: { id: assistantMsgId },
      });

      abortControllerRef.current = new AbortController();

      await streamChat(
        {
          conversation_id: state.conversationId ?? undefined,
          message: content,
        },
        {
          onConversationId: (id) => {
            dispatch({ type: 'SET_CONVERSATION_ID', payload: { id } });
          },
          onContent: (token) => {
            dispatch({ type: 'SET_STATUS', payload: { statusMessage: null } });
            dispatch({ type: 'APPEND_TOKEN', payload: { token } });
          },
          onToolCall: (toolName) => {
            const statusMessage = TOOL_STATUS_MAP[toolName] ?? PHASE_STATUS.DEFAULT;
            dispatch({ type: 'SET_STATUS', payload: { statusMessage } });
          },
          onToolResult: (toolName) => {
            options?.onToolResult?.(toolName);
          },
          onDone: () => {
            dispatch({ type: 'SET_STATUS', payload: { statusMessage: null } });
            dispatch({ type: 'SET_MESSAGE_STATUS', payload: { status: 'completed' } });
            dispatch({ type: 'SET_STREAMING', payload: { isStreaming: false } });
          },
          onError: (error) => {
            dispatch({ type: 'SET_STATUS', payload: { statusMessage: null } });
            dispatch({ type: 'SET_ERROR', payload: { error: error.message } });
            dispatch({ type: 'SET_STREAMING', payload: { isStreaming: false } });
          },
        },
        abortControllerRef.current.signal,
      );
    },
    [state.conversationId, options],
  );

  const stopStreaming = useCallback(() => {
    abortControllerRef.current?.abort();
    dispatch({ type: 'SET_STREAMING', payload: { isStreaming: false } });
    dispatch({ type: 'SET_STATUS', payload: { statusMessage: null } });
    dispatch({ type: 'SET_MESSAGE_STATUS', payload: { status: 'aborted' } });

    const lastUserMessage = [...state.messages].reverse().find((m) => m.role === 'user');
    if (lastUserMessage) {
      options?.onAbort?.(lastUserMessage.content);
    }
  }, [state.messages, options]);

  return {
    messages: state.messages,
    isStreaming: state.isStreaming,
    statusMessage: state.statusMessage,
    error: state.error,
    conversationId: state.conversationId,
    sendMessage,
    stopStreaming,
  };
};
