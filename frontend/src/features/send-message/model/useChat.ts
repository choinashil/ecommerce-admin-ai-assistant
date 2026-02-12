import { useCallback, useReducer } from 'react';

import { streamChat } from '../api/chat-api';

import type { ChatAction, ChatState } from './types';

const initialState: ChatState = {
  messages: [],
  conversationId: null,
  isStreaming: false,
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

    case 'SET_CONVERSATION_ID':
      return { ...state, conversationId: action.payload.id };

    case 'SET_STREAMING':
      return { ...state, isStreaming: action.payload.isStreaming };

    case 'SET_ERROR':
      return { ...state, error: action.payload.error };

    default:
      return state;
  }
};

export const useChat = () => {
  const [state, dispatch] = useReducer(chatReducer, initialState);

  const sendMessage = useCallback(
    async (content: string) => {
      const userMsgId = crypto.randomUUID();
      dispatch({
        type: 'ADD_USER_MESSAGE',
        payload: { id: userMsgId, content },
      });

      dispatch({ type: 'SET_STREAMING', payload: { isStreaming: true } });
      dispatch({ type: 'SET_ERROR', payload: { error: null } });

      const assistantMsgId = crypto.randomUUID();
      dispatch({
        type: 'ADD_ASSISTANT_MESSAGE',
        payload: { id: assistantMsgId },
      });

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
            dispatch({ type: 'APPEND_TOKEN', payload: { token } });
          },
          onDone: () => {
            dispatch({
              type: 'SET_STREAMING',
              payload: { isStreaming: false },
            });
          },
          onError: (error) => {
            dispatch({
              type: 'SET_ERROR',
              payload: { error: error.message },
            });
            dispatch({
              type: 'SET_STREAMING',
              payload: { isStreaming: false },
            });
          },
        },
      );
    },
    [state.conversationId],
  );

  return {
    messages: state.messages,
    isStreaming: state.isStreaming,
    error: state.error,
    conversationId: state.conversationId,
    sendMessage,
  };
};
