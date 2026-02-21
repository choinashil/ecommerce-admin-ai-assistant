import { ONBOARDING_STEPS } from '../model/steps';
import { useOnboardingStore } from '../model/store';

import { getActiveStep } from './utils';

export const useActiveStep = () => {
  const completedMilestones = useOnboardingStore((s) => s.completedMilestones);
  const activeStep = getActiveStep(ONBOARDING_STEPS, completedMilestones)

  return { activeStep };
};
