import { useCallback } from 'react';

import { useQueryClient } from '@tanstack/react-query';

import { productQueries } from '@/entities/product';
import { ChatPanel } from '@/widgets/chat-panel';
import { ProductPanel } from '@/widgets/product-panel';

const PRODUCT_TOOLS = ['create_product', 'list_products'];

const AdminPage = () => {
  const queryClient = useQueryClient();

  const handleToolResult = useCallback(
    (toolName: string) => {
      if (PRODUCT_TOOLS.includes(toolName)) {
        queryClient.invalidateQueries({ queryKey: productQueries.all() });
      }
    },
    [queryClient],
  );

  return (
    <>
      <ProductPanel />
      <ChatPanel onToolResult={handleToolResult} />
    </>
  );
};

export default AdminPage;
