import { Bot, ChevronDown, ChevronRight, Clock, Cpu, User, Wrench, Zap } from 'lucide-react';

import type { MessageDetail } from '@/entities/message';
import { formatDate } from '@/shared/lib/format';
import { Badge } from '@/shared/ui/Badge';
import MarkdownContent from '@/shared/ui/MarkdownContent';

import { isSearchGuideToolCall } from '../model/tool-calls';

import GuideSearchResult from './GuideSearchResult';
import MessageTimelineSkeleton from './MessageTimelineSkeleton';
import SystemPromptCard from './SystemPromptCard';
import ToolCallDefaultResult from './ToolCallDefaultResult';

interface MessageTimelineProps {
  messages: MessageDetail[];
}

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
            <span className='text-xs text-muted-foreground'>{formatDate(message.created_at)}</span>
          </div>

          {message.role === 'user' ? (
            <p className='text-sm whitespace-pre-wrap'>{message.content}</p>
          ) : (
            <MarkdownContent content={message.content} />
          )}

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

          {message.metadata?.tool_calls && message.metadata.tool_calls.length > 0 && (
            <div className='mt-2 space-y-1'>
              {message.metadata.tool_calls.map((toolCall, index) => (
                <details key={index} className='group rounded border bg-muted/30 text-xs'>
                  <summary className='flex cursor-pointer items-center gap-1.5 px-2 py-1.5'>
                    <ChevronRight className='h-3 w-3 text-muted-foreground group-open:hidden' />
                    <ChevronDown className='hidden h-3 w-3 text-muted-foreground group-open:block' />
                    <Wrench className='h-3 w-3 text-muted-foreground' />
                    <span className='font-medium'>{toolCall.name}</span>
                  </summary>
                  <div className='border-t px-2 py-1.5'>
                    {isSearchGuideToolCall(toolCall) ? (
                      <GuideSearchResult toolCall={toolCall} />
                    ) : (
                      <ToolCallDefaultResult toolCall={toolCall} />
                    )}
                  </div>
                </details>
              ))}
            </div>
          )}
        </div>
      ))}
    </div>
  );
};

MessageTimeline.Skeleton = MessageTimelineSkeleton;

export default MessageTimeline;
