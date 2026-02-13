import { useQuery } from '@tanstack/react-query';

import { ProductTable, productQueries } from '@/entities/product';

const ProductPanel = () => {
  const { data: products = [], isLoading, error } = useQuery(productQueries.list());

  return (
    <div className='flex-1 overflow-auto p-6'>
      <h2 className='text-2xl font-bold'>상품 현황</h2>

      <div className='mt-6'>
        {isLoading && <p className='text-muted-foreground'>로딩 중...</p>}
        {error && <p className='text-destructive'>{error.message}</p>}
        {!isLoading && !error && <ProductTable products={products} />}
      </div>
    </div>
  );
};

export default ProductPanel;
