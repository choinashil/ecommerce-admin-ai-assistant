import { create } from 'zustand';
import { persist } from 'zustand/middleware';

import type { OnboardingMilestone } from './types';

interface OnboardingState {
  completedMilestones: OnboardingMilestone[];
  isLocked: boolean;
}

interface OnboardingActions {
  completeMilestone: (milestone: OnboardingMilestone) => void;
  lock: () => void;
  unlock: () => void;
}

type OnboardingStore = OnboardingState & OnboardingActions;

export const useOnboardingStore = create<OnboardingStore>()(
  persist(
    (set, get) => ({
      completedMilestones: [],
      isLocked: false,
      completeMilestone: (milestone) => {
        const { completedMilestones } = get();
        if (completedMilestones.includes(milestone)) {
          return;
        }
        set({ completedMilestones: [...completedMilestones, milestone] });
      },
      lock: () => set({ isLocked: true }),
      unlock: () => set({ isLocked: false }),
    }),
    {
      name: 'onboarding',
      partialize: ({ completedMilestones }) => ({ completedMilestones }),
    },
  ),
);
