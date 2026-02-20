import { useLocation, useNavigate } from 'react-router-dom';

export const useBackNavigation = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const goBack = (fallbackPath: string) => {
    if (location.key !== 'default') {
      navigate(-1);
    } else {
      navigate(fallbackPath);
    }
  };

  return { goBack };
};
