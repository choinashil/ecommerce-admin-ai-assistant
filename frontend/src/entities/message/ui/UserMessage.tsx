interface UserMessageProps {
  content: string;
}

const UserMessage = ({ content }: UserMessageProps) => {
  return (
    <div className='flex justify-end'>
      <div className='max-w-[80%] rounded-lg bg-muted px-3 py-2 text-sm'>
        <p className='whitespace-pre-wrap'>{content}</p>
      </div>
    </div>
  );
};

export default UserMessage;
