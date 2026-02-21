import { useEffect, useRef, useState } from 'react';

import { useActiveStep } from '../lib/useActiveStep';
import { useOnboardingStore } from '../model/store';

import OnboardingTooltip from './OnboardingTooltip';

const OnboardingGuide = () => {
  const { activeStep } = useActiveStep();
  const isLocked = useOnboardingStore((s) => s.isLocked);
  const [targetElement, setTargetElement] = useState<HTMLElement | null>(null);
  const prevSelectorRef = useRef<string | null>(null);

  const selector = activeStep ? `[data-onboarding="${activeStep.targetSelector}"]` : null;

  if (prevSelectorRef.current !== selector) {
    prevSelectorRef.current = selector;
    const el = selector ? document.querySelector<HTMLElement>(selector) : null;
    if (el !== targetElement) {
      setTargetElement(el);
    }
  }

  useEffect(() => {
    if (!selector) {
      return;
    }

    const observer = new MutationObserver(() => {
      const el = document.querySelector<HTMLElement>(selector);
      setTargetElement((prev) => {
        if (el === prev) {
          return prev;
        }
        return el;
      });
    });

    observer.observe(document.body, { childList: true, subtree: true });

    return () => {
      observer.disconnect();
    };
  }, [selector]);

  if (!activeStep || !targetElement || isLocked) {
    return null;
  }

  return <OnboardingTooltip step={activeStep} targetElement={targetElement} />;
};

export default OnboardingGuide;
