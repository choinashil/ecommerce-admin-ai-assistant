export interface SSEEvent {
  type: string;
  data: string;
}

export interface SSERequestOptions {
  url: string;
  body: unknown;
  signal?: AbortSignal;
  headers?: Record<string, string>;
  onEvent: (event: SSEEvent) => void;
  onError: (error: Error) => void;
}

const isAbortError = (error: unknown): boolean =>
  error instanceof DOMException && error.name === 'AbortError';

export const streamSSE = async ({
  url,
  body,
  signal,
  headers: extraHeaders,
  onEvent,
  onError,
}: SSERequestOptions): Promise<void> => {
  let response: Response;

  try {
    response = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...extraHeaders },
      body: JSON.stringify(body),
      signal,
    });
  } catch (error) {
    if (isAbortError(error)) {
      return;
    }
    onError(error instanceof Error ? error : new Error(String(error)));
    return;
  }

  if (!response.ok) {
    const text = await response.text().catch(() => '');
    onError(new Error(`HTTP ${response.status}: ${text || response.statusText}`));
    return;
  }

  const reader = response.body?.getReader();
  if (!reader) {
    onError(new Error('ReadableStream not supported'));
    return;
  }

  const decoder = new TextDecoder();
  let buffer = '';

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) {
        break;
      }

      buffer += decoder.decode(value, { stream: true });

      // SSE 이벤트는 빈 줄(\n\n)로 구분된다
      const events = buffer.split('\n\n');
      // 마지막 요소는 아직 완성되지 않은 이벤트일 수 있으므로 버퍼에 유지
      buffer = events.pop() ?? '';

      for (const event of events) {
        const line = event.trim();
        if (!line.startsWith('data: ')) {
          continue;
        }

        const jsonStr = line.slice('data: '.length);

        try {
          const parsed = JSON.parse(jsonStr) as SSEEvent;
          onEvent(parsed);
        } catch {
          // JSON 파싱 실패 시 무시
        }
      }
    }
  } catch (error) {
    if (isAbortError(error)) {
      return;
    }
    onError(error instanceof Error ? error : new Error(String(error)));
  } finally {
    reader.releaseLock();
  }
};
