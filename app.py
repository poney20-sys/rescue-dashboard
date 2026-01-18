import { DashboardLayout } from '@/components/DashboardLayout';
import { NavigationPanel } from '@/components/NavigationPanel';
import { NewsWidget } from '@/components/NewsWidget';
import { WeatherWidget } from '@/components/WeatherWidget';
import { CalendarWidget } from '@/components/CalendarWidget';
import { EventCreator } from '@/components/EventCreator';
import { ActiveEvents } from '@/components/ActiveEvents';
import { AISidebar } from '@/components/AISidebar';

const Index = () => {
  return (
    <DashboardLayout>
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 pb-12">
        {/* Right Column - Navigation & Event Management */}
        <div className="lg:col-span-5 xl:col-span-4 space-y-6 order-2 lg:order-1">
          <EventCreator />
          <ActiveEvents />
          <NavigationPanel />
        </div>

        {/* Left Column - Info Widgets */}
        <div className="lg:col-span-7 xl:col-span-8 space-y-6 order-1 lg:order-2">
          <NewsWidget />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <WeatherWidget />
            <CalendarWidget />
          </div>
        </div>
      </div>

      {/* AI Sidebar */}
      <AISidebar />
    </DashboardLayout>
  );
};

export default Index;
