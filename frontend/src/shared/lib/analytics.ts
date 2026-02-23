const GA_MEASUREMENT_ID = 'G-N16G8M16N3';

type GtagCommand = 'event' | 'config' | 'js';

declare global {
  interface Window {
    dataLayer?: unknown[];
    gtag?: (...args: [GtagCommand, string | Date, ...unknown[]]) => void;
  }
}

export const GA_EVENTS = {
  SEND_MESSAGE: 'send_message',
  OPEN_CONVERSATION_HISTORY: 'open_conversation_history',
} as const;

export const initGA = () => {
  if (!import.meta.env.PROD) {
    return;
  }

  window.dataLayer = window.dataLayer || [];
  window.gtag = (...args: [GtagCommand, string | Date, ...unknown[]]) => {
    window.dataLayer!.push(args);
  };
  window.gtag('js', new Date());
  window.gtag('config', GA_MEASUREMENT_ID);

  const script = document.createElement('script');
  script.src = `https://www.googletagmanager.com/gtag/js?id=${GA_MEASUREMENT_ID}`;
  script.async = true;
  document.head.appendChild(script);
};

export const trackEvent = (eventName: string, params?: Record<string, unknown>) => {
  window.gtag?.('event', eventName, params);
};
