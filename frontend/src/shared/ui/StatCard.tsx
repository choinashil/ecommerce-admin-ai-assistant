interface StatCardProps {
  icon: React.ReactNode;
  label: string;
  value: string | number;
}

const StatCard = ({ icon, label, value }: StatCardProps) => {
  return (
    <div className='flex items-center gap-3 rounded-lg border bg-background p-4'>
      <div className='text-muted-foreground'>{icon}</div>
      <div>
        <p className='text-sm text-muted-foreground'>{label}</p>
        <p className='text-2xl font-bold tabular-nums'>{value}</p>
      </div>
    </div>
  );
};

export default StatCard;
