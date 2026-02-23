import { Navigate, useParams } from 'react-router-dom';

import { ROUTES } from '@/shared/config/routes';
import { useBackNavigation } from '@/shared/lib/useBackNavigation';
import { SellerDetailPanel } from '@/widgets/seller-panel';

const SellerDetailPage = () => {
  const { id } = useParams<{ id: string }>();
  const { goBack } = useBackNavigation();

  if (!id) {
    return <Navigate to={ROUTES.CONVERSATIONS} replace />;
  }

  return (
    <>
      <title>판매자 상세 | SixPro AI Assistant</title>
      <SellerDetailPanel id={id} onBack={() => goBack(ROUTES.CONVERSATIONS)} />
    </>
  );
};

export default SellerDetailPage;
