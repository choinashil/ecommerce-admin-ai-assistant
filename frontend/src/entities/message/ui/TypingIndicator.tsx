const TypingIndicator = () => {
  return (
    <div className='flex items-center gap-1 px-2 py-1'>
      <span className='h-2 w-2 animate-bounce rounded-full bg-muted-foreground [animation-delay:0ms]' />
      <span className='h-2 w-2 animate-bounce rounded-full bg-muted-foreground [animation-delay:150ms]' />
      <span className='h-2 w-2 animate-bounce rounded-full bg-muted-foreground [animation-delay:300ms]' />
    </div>
  );
};

export default TypingIndicator;
