import type { Message, MessageDetail, MessageRole } from '../model/types';

const CHAT_ROLES: MessageRole[] = ['user', 'assistant'];

const convertToMessage = (detail: MessageDetail): Message => ({
  id: detail.id,
  role: detail.role as MessageRole,
  content: detail.content,
  status: 'completed',
});

export const convertToMessages = (details: MessageDetail[]): Message[] =>
  details.filter((d) => CHAT_ROLES.includes(d.role as MessageRole)).map(convertToMessage);
