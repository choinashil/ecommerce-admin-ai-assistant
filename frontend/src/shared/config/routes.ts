export const ROUTES = {
  HOME: '/',
  CONVERSATIONS: '/conversations',
  CONVERSATION_DETAIL: (id: string | number) => `/conversations/${id}`,
  SELLERS: '/sellers',
  SELLER_DETAIL: (id: string | number) => `/sellers/${id}`,
} as const;

export const isAdminPath = (pathname: string) =>
  pathname.startsWith(ROUTES.CONVERSATIONS) || pathname.startsWith(ROUTES.SELLERS);
