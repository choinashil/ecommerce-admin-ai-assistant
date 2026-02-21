import { autoUpdate, flip, offset, shift, useFloating } from '@floating-ui/react-dom';
import { X } from 'lucide-react';

import { cn } from '@/shared/lib/utils';
import { Button } from '@/shared/ui/Button';

import { useOnboardingStore } from '../model/store';

import type { OnboardingStep } from '../model/types';

interface OnboardingTooltipProps {
  step: OnboardingStep;
  targetElement: HTMLElement;
}

const OnboardingTooltip = ({ step, targetElement }: OnboardingTooltipProps) => {
  const skipStep = () => {
    useOnboardingStore.getState().completeMilestone(step.milestone);
  };

  const { refs, floatingStyles } = useFloating({
    elements: { reference: targetElement },
    placement: step.placement,
    middleware: [offset(step.offset ?? 8), flip(), shift({ padding: 8 })],
    whileElementsMounted: autoUpdate,
  });

  return (
    <div
      // eslint-disable-next-line react-hooks/refs
      ref={refs.setFloating}
      role='tooltip'
      className='fixed z-[100] w-64'
      style={floatingStyles}
    >
      <div className='animate-bounce hover:paused'>
        <div
          className={cn(
            'animate-shimmer rounded-xl border-[1.5px] border-transparent bg-clip-padding p-3',
            'shadow-lg shadow-violet-500/20',
          )}
          style={{
            backgroundImage:
              'linear-gradient(var(--popover), var(--popover)), linear-gradient(to right, #8b5cf6, #ec4899, #8b5cf6)',
            backgroundOrigin: 'padding-box, border-box',
            backgroundClip: 'padding-box, border-box',
            backgroundSize: '100% 100%, 200% 100%',
          }}
        >
          <div className='flex items-start justify-between gap-2'>
            <div>
              <p className='text-sm font-medium'>{step.title}</p>
              <p className='mt-1 text-xs text-muted-foreground'>{step.description}</p>
            </div>
            <Button
              variant='ghost'
              size='icon-xs'
              onClick={skipStep}
              aria-label='이 가이드 건너뛰기'
            >
              <X className='h-3 w-3' />
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OnboardingTooltip;
