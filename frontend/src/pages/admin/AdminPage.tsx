import { useCallback, useRef, useState } from 'react';

import { useQueryClient } from '@tanstack/react-query';

import { productQueries } from '@/entities/product';
import { useOnboardingStore } from '@/features/onboarding';
import { ChatPanel } from '@/widgets/chat-panel';
import { ProductPanel } from '@/widgets/product-panel';

const PRODUCT_TOOLS = ['create_product', 'list_products'];

const AdminPage = () => {
  const queryClient = useQueryClient();

  const [inputValue, setInputValue] = useState('');
  const inputRef = useRef<HTMLInputElement>(null);

  const handleSelectPrompt = (prompt: string) => {
    setInputValue(prompt);
    inputRef.current?.focus();
  };

  const handleToolResult = useCallback(
    (toolName: string) => {
      if (PRODUCT_TOOLS.includes(toolName)) {
        queryClient.invalidateQueries({ queryKey: productQueries.all() });
      }

      if (toolName === 'create_product') {
        useOnboardingStore.getState().completeMilestone('product_created');
      }
    },
    [queryClient],
  );

  return (
    <>
      <ProductPanel onSelectPrompt={handleSelectPrompt} />
      <ChatPanel
        onToolResult={handleToolResult}
        inputValue={inputValue}
        onInputChange={setInputValue}
        inputRef={inputRef}
        onSelectPrompt={handleSelectPrompt}
      />
    </>
  );
};

export default AdminPage;
