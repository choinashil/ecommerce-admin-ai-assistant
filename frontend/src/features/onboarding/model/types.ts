export type OnboardingMilestone = 'guide_searched' | 'product_created' | 'admin_visited';

export interface OnboardingStep {
  milestone: OnboardingMilestone;
  targetSelector: string;
  title: string;
  description: string;
  placement: 'top' | 'bottom' | 'left' | 'right';
  offset?: number;
  prerequisites: OnboardingMilestone[];
}
