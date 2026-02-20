import { ErrorBoundary, Suspense } from '@suspensive/react';
import { SuspenseQuery } from '@suspensive/react-query';

import { ProductTable, productQueries } from '@/entities/product';

const ProductPanel = () => {
  return (
    <div className='flex-1 overflow-auto rounded-t-2xl bg-background p-6 shadow-sm'>
      <h2 className='text-2xl font-bold'>상품 관리</h2>

      <div className='mt-6'>
        <ErrorBoundary
          fallback={({ error }) => <p className='text-destructive'>{error.message}</p>}
        >
          <Suspense fallback={<p className='text-muted-foreground'>로딩 중...</p>}>
            <SuspenseQuery {...productQueries.list()}>
              {({ data: products }) => <ProductTable products={products} />}
            </SuspenseQuery>
          </Suspense>
        </ErrorBoundary>
      </div>
    </div>
  );
};

export default ProductPanel;
