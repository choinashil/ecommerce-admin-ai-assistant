import ApiError from '@/shared/api/api-error';
import client from '@/shared/api/client';

export const createSeller = async () => {
  const { data, error, response } = await client.POST('/api/sellers');

  if (error) {
    throw new ApiError(response.status, error, '판매자 생성에 실패했습니다.');
  }

  return data;
};
