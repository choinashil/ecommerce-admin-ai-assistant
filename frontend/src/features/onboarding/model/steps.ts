import type { OnboardingStep } from './types';

export const ONBOARDING_STEPS: OnboardingStep[] = [
  {
    milestone: 'guide_searched',
    targetSelector: 'chat-empty-state',
    title: '가이드를 검색해보세요',
    description: '위 추천 프롬프트를 클릭하면 쇼핑몰 운영 가이드를 AI가 검색해줍니다.',
    placement: 'bottom',
    offset: 40,
    prerequisites: [],
  },
  {
    milestone: 'product_created',
    targetSelector: 'product-empty-state',
    title: '첫 상품을 등록해보세요',
    description: '채팅으로 AI에게 상품 등록을 요청하면 자동으로 등록됩니다.',
    placement: 'bottom',
    offset: 40,
    prerequisites: ['guide_searched'],
  },
  {
    milestone: 'admin_visited',
    targetSelector: 'profile-menu',
    title: '관리자 페이지를 둘러보세요',
    description: '프로필 메뉴에서 관리자를 선택하면 대화 로그를 확인할 수 있습니다.',
    placement: 'bottom',
    offset: 16,
    prerequisites: ['product_created'],
  },
];
