import type { Product } from '@/entities/product';
import { formatDate, formatPrice } from '@/shared/lib/format';
import { Badge } from '@/shared/ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/shared/ui/table';

interface ProductTableProps {
  products: Product[];
}

const ProductTable = ({ products }: ProductTableProps) => {
  if (products.length === 0) {
    return <p className='text-muted-foreground'>등록된 상품이 없습니다.</p>;
  }

  return (
    <Table>
      <TableHeader>
        <TableRow>
          <TableHead>ID</TableHead>
          <TableHead className='w-1/4'>상품명</TableHead>
          <TableHead>가격</TableHead>
          <TableHead>상태</TableHead>
          <TableHead>등록일시</TableHead>
        </TableRow>
      </TableHeader>
      <TableBody>
        {products.map((product) => (
          <TableRow key={product.id}>
            <TableCell className='font-mono'>{product.id}</TableCell>
            <TableCell>{product.name}</TableCell>
            <TableCell className='tabular-nums'>{formatPrice(product.price)}원</TableCell>
            <TableCell>
              {product.status === 'active' ? (
                <Badge variant='default'>판매중</Badge>
              ) : (
                <Badge variant='secondary'>비활성</Badge>
              )}
            </TableCell>
            <TableCell>{formatDate(product.created_at)}</TableCell>
          </TableRow>
        ))}
      </TableBody>
    </Table>
  );
};

export default ProductTable;
