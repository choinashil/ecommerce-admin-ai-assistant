import ApiError from '@/shared/api/api-error';
import client from '@/shared/api/client';

export const fetchProducts = async () => {
  const { data, error, response } = await client.GET('/api/products');
  const { status } = response;

  if (error) {
    throw new ApiError(status, error, '상품 목록을 불러오는데 실패했습니다.');
  }

  return data;
};
