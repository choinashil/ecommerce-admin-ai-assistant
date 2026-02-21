import { ErrorBoundary, Suspense } from '@suspensive/react';
import { SuspenseQuery } from '@suspensive/react-query-5';

import { ProductTable, productQueries } from '@/entities/product';
import { useOnboardingStore } from '@/features/onboarding';
import { SuggestedPrompts } from '@/features/suggested-prompts';

interface ProductPanelProps {
  onSelectPrompt: (prompt: string) => void;
}

const ProductPanel = ({ onSelectPrompt }: ProductPanelProps) => {
  const isProductStepReady = useOnboardingStore(
    (s) => s.completedMilestones.includes('guide_searched') && !s.isLocked,
  );

  return (
    <div className='flex flex-1 flex-col overflow-auto rounded-t-2xl bg-background p-6 shadow-sm'>
      <h2 className='text-2xl font-bold'>상품 관리</h2>
      <div className='mt-6 flex flex-1 flex-col'>
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
                          <p className='text-sm text-muted-foreground'>
                            아직 등록된 상품이 없어요.
                          </p>
                          {isProductStepReady && (
                            <p className='text-lg font-medium text-foreground'>
                              AI 채팅으로 간편하게 등록해보세요.
                            </p>
                          )}
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
