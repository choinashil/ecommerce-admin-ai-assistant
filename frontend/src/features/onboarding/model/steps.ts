import type { OnboardingStep } from './types';

export const ONBOARDING_STEPS: OnboardingStep[] = [
  {
    milestone: 'guide_searched',
    targetSelector: 'chat-empty-state',
    title: '쇼핑몰 운영 가이드를 검색해보세요',
    description: '추천 프롬프트를 선택하거나 직접 입력하면 AI가 가이드 문서를 검색해 답변해드립니다.',
    placement: 'top',
    offset: 32,
    prerequisites: [],
  },
  {
    milestone: 'product_created',
    targetSelector: 'product-empty-state',
    title: '첫 상품을 등록해보세요.',
    description: 'AI 채팅으로 등록하고, 수정·삭제까지 관리할 수 있어요.',
    placement: 'top',
    offset: 32,
    prerequisites: ['guide_searched'],
  },
  {
    milestone: 'admin_visited',
    targetSelector: 'profile-menu',
    title: 'LLM 로그를 확인해보세요',
    description: '프로필 메뉴에서 관리자를 선택하면 볼 수 있어요.',
    placement: 'bottom',
    offset: 16,
    prerequisites: ['product_created'],
  },
];
