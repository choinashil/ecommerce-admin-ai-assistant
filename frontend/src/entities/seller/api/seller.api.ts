import ApiError from '@/shared/api/api-error';
import client from '@/shared/api/client';

export const fetchSellerDetail = async (sellerId: string) => {
  const { data, error, response } = await client.GET('/api/sellers/{seller_id}', {
    params: { path: { seller_id: sellerId } },
  });

  if (error) {
    throw new ApiError(response.status, error, '판매자 정보를 불러오는데 실패했습니다.');
  }

  return data;
};
