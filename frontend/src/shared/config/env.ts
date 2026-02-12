const requireEnv = (key: string): string => {
  const value = import.meta.env[key];

  if (!value) {
    throw new Error(`${key} 환경변수가 설정되지 않았습니다. .env 파일을 확인하세요.`);
  }

  return value;
};

const env = {
  API_BASE_URL: requireEnv('VITE_API_BASE_URL'),
} as const;

export default env;
