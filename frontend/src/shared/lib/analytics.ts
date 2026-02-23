type GtagCommand = 'event' | 'config' | 'js';

declare global {
  interface Window {
    gtag?: (...args: [GtagCommand, string, ...unknown[]]) => void;
  }
}

export const GA_EVENTS = {
  SEND_MESSAGE: 'send_message',
  OPEN_CONVERSATION_HISTORY: 'open_conversation_history',
} as const;

const isProduction = import.meta.env.PROD;

export const trackEvent = (eventName: string, params?: Record<string, unknown>) => {
  if (!isProduction) {
    return;
  }

  window.gtag?.('event', eventName, params);
};

