import createClient from 'openapi-fetch';

import type { paths } from '@/shared/api/schema';
import env from '@/shared/config/env';

const client = createClient<paths>({ baseUrl: env.API_BASE_URL });

export default client;
