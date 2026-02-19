import ApiError from '@/shared/api/api-error';
import client from '@/shared/api/client';

export const fetchMessages = async (conversationId: string) => {
  const { data, error, response } = await client.GET('/api/conversations/{display_id}/messages', {
    params: { path: { display_id: conversationId } },
  });

  if (error) {
    throw new ApiError(response.status, error, '메시지를 불러오는데 실패했습니다.');
  }

  return data;
};
