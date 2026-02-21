import type { OnboardingMilestone, OnboardingStep } from '../model/types';

export const getActiveStep = (
  steps: OnboardingStep[],
  completedMilestones: OnboardingMilestone[],
): OnboardingStep | null =>
  steps.find(
    (step) =>
      !completedMilestones.includes(step.milestone) &&
      step.prerequisites.every((prerequisite) => completedMilestones.includes(prerequisite)),
  ) ?? null;
