import { ExternalLink, FileText, Search } from 'lucide-react';

import { Badge } from '@/shared/ui/Badge';

import type { SearchGuideToolCall } from '../model/tool-calls';

interface GuideSearchResultProps {
  toolCall: SearchGuideToolCall;
}

const GuideSearchResult = ({
  toolCall: {
    arguments: { query },
    result: { results },
  },
}: GuideSearchResultProps) => {
  return (
    <div className='space-y-1.5'>
      <div className='flex items-center gap-1.5 text-muted-foreground'>
        <Search className='h-3 w-3' />
        <span>검색어: &quot;{query}&quot;</span>
      </div>

      <div className='flex items-center gap-1.5 text-muted-foreground'>
        <FileText className='h-3 w-3' />
        <span>검색 결과</span>
        <Badge variant='secondary' className='text-[10px]'>
          {results.length}건
        </Badge>
      </div>

      <div className='rounded bg-muted p-2'>
        <ul className='list-disc space-y-1 pl-4 marker:text-muted-foreground'>
          {results.map((result) => (
            <li key={result.url}>
              <div className='flex items-center gap-2'>
                <a
                  href={result.url}
                  target='_blank'
                  rel='noopener noreferrer'
                  className='inline-flex items-center gap-1 font-medium text-blue-500 hover:underline'
                >
                  {result.title}
                  <ExternalLink className='h-3 w-3' />
                </a>
                <Badge variant='outline' className='text-[10px]'>
                  유사도 {Math.round(result.similarity * 100)}%
                </Badge>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default GuideSearchResult;
