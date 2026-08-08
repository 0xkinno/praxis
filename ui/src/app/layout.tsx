import './globals.css';
import LayoutWrapper from '@/components/layout/LayoutWrapper';

export const metadata = {
  title: 'PRAXIS | Data Trust Intelligence',
  description: 'Continuous Data Trust Intelligence for DataHub',
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <LayoutWrapper>
          {children}
        </LayoutWrapper>
      </body>
    </html>
  );
}
