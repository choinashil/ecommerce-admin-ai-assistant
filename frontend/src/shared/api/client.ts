import createClient from 'openapi-fetch';

import { getToken } from '@/entities/seller';
import type { paths } from '@/shared/api/schema';
import env from '@/shared/config/env';

const client = createClient<paths>({ baseUrl: env.API_BASE_URL });

client.use({
  onRequest({ request }) {
    const token = getToken();
    if (token) {
      request.headers.set('Authorization', `Bearer ${token}`);
    }
    return request;
  },
});

export default client;
