import { describe, expect, test } from 'vitest';

import { pickRandomPrompts } from '../utils';

describe('pickRandomPrompts', () => {
  test('요청한 개수만큼 프롬프트를 반환한다', () => {
    const result = pickRandomPrompts(3);

    expect(result).toHaveLength(3);
  });

  test('중복 없이 반환한다', () => {
    const result = pickRandomPrompts(3, 'guide');
    const unique = new Set(result);

    expect(unique.size).toBe(result.length);
  });

  test('count가 0이면 빈 배열을 반환한다', () => {
    const result = pickRandomPrompts(0);

    expect(result).toEqual([]);
  });
});
