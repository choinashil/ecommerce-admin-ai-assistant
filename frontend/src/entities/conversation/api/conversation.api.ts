import ApiError from '@/shared/api/api-error';
import client from '@/shared/api/client';

export const fetchConversations = async () => {
  const { data, error, response } = await client.GET('/api/conversations');
  const { status } = response;

  if (error) {
    throw new ApiError(status, error, '대화 목록을 불러오는데 실패했습니다.');
  }

  return data;
};
