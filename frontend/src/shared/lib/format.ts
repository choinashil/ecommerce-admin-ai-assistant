export const formatPrice = (price: number) => {
  return price.toLocaleString('ko-KR');
};

export const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleString('ko-KR', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  });
};
