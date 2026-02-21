const FRUIT_NAMES = [
  '사과',
  '배',
  '포도',
  '딸기',
  '수박',
  '참외',
  '복숭아',
  '자두',
  '체리',
  '블루베리',
  '망고',
  '바나나',
  '키위',
  '레몬',
  '오렌지',
  '귤',
  '자몽',
  '파인애플',
  '아보카도',
  '석류',
  '감',
  '매실',
  '살구',
  '무화과',
  '라즈베리',
] as const;

const REGISTER_TEMPLATES = [
  (name: string, price: number) => `${name} ${price.toLocaleString()}원에 등록해주세요`,
  (name: string, price: number) => `${name} 상품 추가해줘, 가격은 ${price.toLocaleString()}원`,
  (name: string, price: number) => `새 상품 등록 - ${name} ${price.toLocaleString()}원`,
  (name: string, price: number) => `${name} ${price.toLocaleString()}원짜리 만들어줘`,
  (name: string, price: number) => `${name} 하나 올려줘 ${price.toLocaleString()}원으로`,
  (name: string, price: number) => `${name} ${price.toLocaleString()}원으로 상품 생성해주세요`,
  (name: string, price: number) => `${name} ${price.toLocaleString()}원으로 추가해줘`,
];

const randomInt = (min: number, max: number): number =>
  Math.floor(Math.random() * (max - min + 1)) + min;

export const generateProductCreatePrompt = (): string => {
  const fruit = FRUIT_NAMES[randomInt(0, FRUIT_NAMES.length - 1)];
  const price = randomInt(1, 50) * 1000;
  const template = REGISTER_TEMPLATES[randomInt(0, REGISTER_TEMPLATES.length - 1)];
  return template(fruit, price);
};

export const PRODUCT_QUERY_PROMPTS: string[] = [
  '등록된 상품 목록 보여줘',
  '현재 판매 중인 상품 알려줘',
  '판매중지된 상품 있어?',
  '포도는 얼마야?',
  '사과 가격 알려줘',
  '지금 상품 몇 개 등록되어 있어?',
  '가장 비싼 상품이 뭐야?',
  '1만원 이하 상품 보여줘',
  '오늘 등록된 상품 있어?',
  '상품 전체 조회해줘',
  '활성 상태인 상품만 알려줘',
  '상품 목록 좀 볼 수 있을까?',
  '바나나 등록되어 있어?',
  '5천원짜리 상품 있어?',
  '최근에 등록한 상품 보여줘',
  '오렌지 판매 상태 알려줘'
];
