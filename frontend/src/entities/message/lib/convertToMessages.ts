import type { Message, MessageDetail, MessageRole, MessageStatus } from '../model/types';

const CHAT_ROLES: MessageRole[] = ['user', 'assistant'];

const getStatus = (detail: MessageDetail): MessageStatus => {
  if (detail.metadata?.aborted) {
    return 'aborted';
  }
  return 'completed';
};

const convertToMessage = (detail: MessageDetail): Message => ({
  id: detail.id,
  role: detail.role as MessageRole,
  content: detail.content,
  status: getStatus(detail),
});

export const convertToMessages = (details: MessageDetail[]): Message[] =>
  details.filter((d) => CHAT_ROLES.includes(d.role as MessageRole)).map(convertToMessage);
