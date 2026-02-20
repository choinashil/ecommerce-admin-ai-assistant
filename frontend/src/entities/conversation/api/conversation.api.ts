import ApiError from '@/shared/api/api-error';
import client from '@/shared/api/client';

export const fetchConversations = async (sellerId?: string) => {
  const { data, error, response } = await client.GET('/api/conversations', {
    params: { query: sellerId ? { seller_id: sellerId } : {} },
  });

  if (error) {
    throw new ApiError(response.status, error, '대화 목록을 불러오는데 실패했습니다.');
  }

  return data;
};

export const fetchMyConversations = async () => {
  const { data, error, response } = await client.GET('/api/my/conversations');

  if (error) {
    throw new ApiError(response.status, error, '대화 목록을 불러오는데 실패했습니다.');
  }

  return data;
};
