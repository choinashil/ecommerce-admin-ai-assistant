import type { components } from '@/shared/api/schema';

export interface SellerSession {
  token: string;
  nickname: string;
}

export type SellerDetail = components['schemas']['SellerDetail'];
