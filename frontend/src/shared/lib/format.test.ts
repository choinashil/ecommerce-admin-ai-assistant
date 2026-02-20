import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';

import { formatDate, formatPrice, formatRelativeTime } from './format';

describe('formatPrice', () => {
  test('천 단위 구분자를 추가한다', () => {
    expect(formatPrice(1000)).toBe('1,000');
    expect(formatPrice(1234567)).toBe('1,234,567');
  });

  test('1000 미만은 그대로 반환한다', () => {
    expect(formatPrice(0)).toBe('0');
    expect(formatPrice(999)).toBe('999');
  });
});

describe('formatDate', () => {
  test('yyyy.MM.dd HH:mm 형식으로 반환한다', () => {
    // 2026-02-20T04:26:00Z = KST 2026-02-20 13:26
    expect(formatDate('2026-02-20T04:26:00Z')).toBe('2026.02.20 13:26');
  });

  test('한 자리 시/분에 0을 패딩한다', () => {
    // 2026-01-05T00:05:00Z = KST 2026-01-05 09:05
    expect(formatDate('2026-01-05T00:05:00Z')).toBe('2026.01.05 09:05');
  });

  test('자정(00:00)을 올바르게 표시한다', () => {
    // 2026-03-15T15:00:00Z = KST 2026-03-16 00:00
    expect(formatDate('2026-03-15T15:00:00Z')).toBe('2026.03.16 00:00');
  });
});

describe('formatRelativeTime', () => {
  const NOW = new Date('2026-02-20T04:00:00Z');

  beforeEach(() => {
    vi.useFakeTimers();
    vi.setSystemTime(NOW);
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  test('1분 미만이면 "방금 전"을 반환한다', () => {
    expect(formatRelativeTime('2026-02-20T03:59:30Z')).toBe('방금 전');
  });

  test('1분 이상 60분 미만이면 "N분 전"을 반환한다', () => {
    expect(formatRelativeTime('2026-02-20T03:55:00Z')).toBe('5분 전');
    expect(formatRelativeTime('2026-02-20T03:01:00Z')).toBe('59분 전');
  });

  test('1시간 이상 24시간 미만이면 "N시간 전"을 반환한다', () => {
    expect(formatRelativeTime('2026-02-20T02:00:00Z')).toBe('2시간 전');
    expect(formatRelativeTime('2026-02-19T05:00:00Z')).toBe('23시간 전');
  });

  test('1일 전이면 "어제"를 반환한다', () => {
    expect(formatRelativeTime('2026-02-19T04:00:00Z')).toBe('어제');
  });

  test('2~6일 전이면 "N일 전"을 반환한다', () => {
    expect(formatRelativeTime('2026-02-18T04:00:00Z')).toBe('2일 전');
    expect(formatRelativeTime('2026-02-14T04:00:00Z')).toBe('6일 전');
  });

  test('7일 이상이면 formatDate 형식으로 반환한다', () => {
    expect(formatRelativeTime('2026-02-13T04:00:00Z')).toBe('2026.02.13 13:00');
    expect(formatRelativeTime('2026-01-01T00:00:00Z')).toBe('2026.01.01 09:00');
  });
});
