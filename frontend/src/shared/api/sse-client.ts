export interface SSERequestOptions {
  url: string;
  body: unknown;
  onEvent: (event: { type: string; data: string }) => void;
  onError: (error: Error) => void;
}

export const streamSSE = async ({
  url,
  body,
  onEvent,
  onError,
}: SSERequestOptions): Promise<void> => {
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    onError(new Error(`HTTP ${response.status}: ${response.statusText}`));
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
          const parsed = JSON.parse(jsonStr) as { type: string; data: string };
          onEvent(parsed);
        } catch {
          // JSON 파싱 실패 시 무시
        }
      }
    }
  } catch (error) {
    onError(error instanceof Error ? error : new Error(String(error)));
  } finally {
    reader.releaseLock();
  }
};
