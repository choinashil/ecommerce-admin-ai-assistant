import { ErrorBoundary, Suspense } from '@suspensive/react';
import { SuspenseQuery } from '@suspensive/react-query-5';
import { CircleHelp } from 'lucide-react';

import { ProductTable, productQueries } from '@/entities/product';
import { useOnboardingStore } from '@/features/onboarding';
import { SuggestedPrompts } from '@/features/suggested-prompts';
import { Tooltip, TooltipContent, TooltipTrigger } from '@/shared/ui/Tooltip';

interface ProductPanelProps {
  onSelectPrompt: (prompt: string) => void;
}

const ProductPanel = ({ onSelectPrompt }: ProductPanelProps) => {
  const isProductStepReady = useOnboardingStore(
    (s) => s.completedMilestones.includes('guide_searched') && !s.isLocked,
  );

  return (
    <div className='flex flex-1 flex-col overflow-auto rounded-t-2xl bg-background shadow-sm'>
      <header className='flex items-center gap-2 px-5 pt-4 pb-3'>
        <h2 className='text-xl font-semibold'>상품 관리</h2>
        <Tooltip>
          <TooltipTrigger asChild>
            <CircleHelp className='size-4 cursor-help text-muted-foreground' />
          </TooltipTrigger>
          <TooltipContent side='right'>AI 채팅으로 상품을 관리해보세요</TooltipContent>
        </Tooltip>
      </header>
      <div className='flex flex-1 flex-col px-4 pb-3'>
        <ErrorBoundary
          fallback={({ error }) => <p className='text-destructive'>{error.message}</p>}
        >
          <Suspense fallback={<ProductTable.Skeleton />}>
            <SuspenseQuery {...productQueries.list()}>
              {({ data: products }) => (
                <>
                  {products.length === 0 ? (
                    <div className='flex flex-1 items-center justify-center pb-[15%]'>
                      <div
                        data-onboarding='product-empty-state'
                        className='flex flex-col gap-6 px-4'
                      >
                        <div className='flex flex-col items-center'>
                          <p className='text-lg font-medium text-foreground'>
                            아직 등록된 상품이 없어요.
                          </p>
                        </div>
                        {isProductStepReady && (
                          <SuggestedPrompts
                            variant='centered'
                            onSelect={onSelectPrompt}
                            isDisabled={false}
                            categoryFilter='product_create'
                          />
                        )}
                      </div>
                    </div>
                  ) : (
                    <ProductTable products={products} />
                  )}
                </>
              )}
            </SuspenseQuery>
          </Suspense>
        </ErrorBoundary>
      </div>
    </div>
  );
};

export default ProductPanel;
