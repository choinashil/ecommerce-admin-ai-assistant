import { Bot, Clock, Cpu, User, Zap } from 'lucide-react';

import type { MessageDetail } from '@/entities/message';
import { Badge } from '@/shared/ui/badge';

import SystemPromptCard from './SystemPromptCard';

interface MessageTimelineProps {
  messages: MessageDetail[];
}

const formatTime = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleTimeString('ko-KR', {
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
  });
};

const MessageTimeline = ({ messages }: MessageTimelineProps) => {
  const systemPrompt = messages.find((m) => m.role === 'assistant' && m.metadata?.system_prompt)
    ?.metadata?.system_prompt;

  return (
    <div className='space-y-4'>
      {systemPrompt && <SystemPromptCard prompt={systemPrompt} />}

      {messages.map((message) => (
        <div key={message.id} className='rounded-md border p-4'>
          <div className='mb-2 flex items-center gap-2'>
            {message.role === 'user' ? (
              <User className='h-4 w-4 text-blue-500' />
            ) : (
              <Bot className='h-4 w-4 text-green-500' />
            )}
            <span className='text-sm font-medium uppercase'>{message.role}</span>
            <span className='text-xs text-muted-foreground'>{formatTime(message.created_at)}</span>
          </div>

          <p className='text-sm whitespace-pre-wrap'>{message.content}</p>

          {message.role === 'assistant' && message.metadata && (
            <div className='mt-3 flex flex-wrap gap-2 border-t pt-3'>
              <Badge variant='outline'>
                <Cpu data-icon='inline-start' />
                {message.metadata.model}
              </Badge>
              {message.metadata.input_tokens != null && message.metadata.output_tokens != null && (
                <Badge variant='secondary'>
                  <Zap data-icon='inline-start' />
                  {message.metadata.input_tokens}→{message.metadata.output_tokens}
                </Badge>
              )}
              {message.metadata.response_time_ms != null && (
                <Badge variant='secondary'>
                  <Clock data-icon='inline-start' />
                  {message.metadata.response_time_ms.toLocaleString()}ms
                </Badge>
              )}
              {message.metadata.error && (
                <Badge variant='destructive'>에러: {message.metadata.error}</Badge>
              )}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

export default MessageTimeline;
