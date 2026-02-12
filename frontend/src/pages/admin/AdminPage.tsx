import { AdminSidebar } from '@/widgets/admin-sidebar';
import { ChatPanel } from '@/widgets/chat-panel';

const AdminPage = () => {
  return (
    <div className='flex h-screen'>
      <AdminSidebar />

      <main className='flex-1 overflow-auto p-6'>
        <h1 className='text-2xl font-bold'>대시보드</h1>
        <p className='mt-2 text-muted-foreground'>상품/주문 요약 (추후 구현)</p>
      </main>

      <ChatPanel />
    </div>
  );
};

export default AdminPage;
