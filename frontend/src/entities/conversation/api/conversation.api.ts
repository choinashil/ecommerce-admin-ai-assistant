import client from '@/shared/api/client';

export const fetchConversations = async () => {
  const { data, error } = await client.GET('/api/conversations');

  if (error) {
    throw new Error('대화 목록을 불러오는데 실패했습니다.');
  }

  return data;
};
