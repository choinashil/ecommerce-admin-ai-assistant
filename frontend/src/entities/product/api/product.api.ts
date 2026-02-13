import client from '@/shared/api/client';

export const fetchProducts = async () => {
  const { data, error } = await client.GET('/api/products');

  if (error) {
    throw new Error('상품 목록을 불러오는데 실패했습니다.');
  }

  return data;
};
