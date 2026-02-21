import { describe, expect, test } from 'vitest';

import { getActiveStep } from '../utils';

import type { OnboardingMilestone, OnboardingStep } from '../../model/types';

const STEPS: OnboardingStep[] = [
  {
    milestone: 'guide_searched',
    targetSelector: 'chat-empty-state',
    title: '1단계',
    description: '',
    placement: 'top',
    prerequisites: [],
  },
  {
    milestone: 'product_created',
    targetSelector: 'product-empty-state',
    title: '2단계',
    description: '',
    placement: 'right',
    prerequisites: ['guide_searched'],
  },
  {
    milestone: 'admin_visited',
    targetSelector: 'profile-menu',
    title: '3단계',
    description: '',
    placement: 'bottom',
    prerequisites: ['product_created'],
  },
];

describe('getActiveStep', () => {
  test('아무것도 완료하지 않으면 첫 번째 스텝을 반환한다', () => {
    const result = getActiveStep(STEPS, []);

    expect(result?.milestone).toBe('guide_searched');
  });

  test('첫 번째 마일스톤 완료 시 두 번째 스텝을 반환한다', () => {
    const result = getActiveStep(STEPS, ['guide_searched']);

    expect(result?.milestone).toBe('product_created');
  });

  test('선행 조건이 충족되지 않으면 해당 스텝을 건너뛴다', () => {
    const result = getActiveStep(STEPS, ['product_created']);

    expect(result?.milestone).toBe('guide_searched');
  });

  test('모든 마일스톤 완료 시 null을 반환한다', () => {
    const all: OnboardingMilestone[] = ['guide_searched', 'product_created', 'admin_visited'];
    const result = getActiveStep(STEPS, all);

    expect(result).toBeNull();
  });

  test('빈 스텝 배열이면 null을 반환한다', () => {
    const result = getActiveStep([], []);

    expect(result).toBeNull();
  });
});
