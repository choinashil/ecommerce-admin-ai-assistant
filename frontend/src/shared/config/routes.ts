export const ROUTES = {
  HOME: '/',
  CONVERSATIONS: '/conversations',
  CONVERSATION_DETAIL: (id: string | number) => `/conversations/${id}`,
} as const;

export const isAdminPath = (pathname: string) =>
  pathname.startsWith(ROUTES.CONVERSATIONS);
