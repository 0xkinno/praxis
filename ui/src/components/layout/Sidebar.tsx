'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { motion } from 'framer-motion';
import { LayoutDashboard, Network, ShieldCheck, FileText, ClipboardList } from 'lucide-react';

export default function Sidebar() {
  const pathname = usePathname();
  
  const navItems = [
    { href: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { href: '/contracts', label: 'Code & Contracts', icon: FileText },
    { href: '/ml-gate', label: 'ML Integrity Gate', icon: ShieldCheck },
    { href: '/propagation', label: 'Downstream Cascade', icon: Network },
    { href: '/assessments', label: 'Daily digests', icon: ClipboardList }
  ];

  return (
    <aside style={{
      width: '280px',
      background: 'var(--bg-glass-secondary)',
      borderRight: '1px solid var(--border-color)',
      display: 'flex',
      flexDirection: 'column',
      height: '100vh',
      position: 'sticky',
      top: 0
    }}>
      
      {/* Clickable PRAXIS logo returning to landing page with cinematic transitions */}
      <Link href="/" style={{ textDecoration: 'none' }}>
        <motion.div
          whileHover={{ x: 3 }}
          transition={{ type: 'spring', stiffness: 300, damping: 20 }}
          style={{
            padding: '32px 24px',
            borderBottom: '1px solid var(--border-color)',
            cursor: 'pointer',
            display: 'flex',
            flexDirection: 'column',
            gap: '4px'
          }}
        >
          <h1 style={{
            fontSize: '20px',
            fontWeight: 600,
            color: 'var(--text-primary)',
            letterSpacing: '0.08em',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            fontFamily: 'var(--font-sans)',
            textTransform: 'uppercase',
            position: 'relative'
          }}>
            <span style={{ width: '8px', height: '8px', borderRadius: '50%', background: 'var(--accent-indigo)', boxShadow: '0 0 10px rgba(44, 27, 140, 0.3)' }}></span>
            PRAXIS
          </h1>
          <span style={{ fontSize: '11px', color: 'var(--text-muted)', letterSpacing: '0.05em' }}>Return to presentation</span>
        </motion.div>
      </Link>
      
      <nav style={{ flex: 1, padding: '32px 16px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {navItems.map(item => {
          const Icon = item.icon;
          const isActive = pathname === item.href;
          return (
            <Link key={item.href} href={item.href} style={{ textDecoration: 'none' }}>
              <button
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '12px',
                  width: '100%',
                  padding: '12px 20px',
                  border: 'none',
                  borderRadius: '100px',
                  background: isActive ? 'rgba(255, 255, 255, 0.75)' : 'transparent',
                  color: isActive ? 'var(--accent-indigo)' : 'var(--text-secondary)',
                  fontSize: '14px',
                  fontWeight: isActive ? 600 : 400,
                  textAlign: 'left',
                  cursor: 'pointer',
                  transition: 'all 0.4s cubic-bezier(0.16, 1, 0.3, 1)',
                  position: 'relative',
                  borderLeft: isActive ? '3px solid var(--accent-indigo)' : '3px solid transparent',
                  paddingLeft: isActive ? '17px' : '20px',
                  boxShadow: isActive ? '0 4px 16px rgba(44, 27, 140, 0.05)' : 'none'
                }}
              >
                <Icon size={16} color={isActive ? 'var(--accent-indigo)' : 'var(--text-secondary)'} />
                {item.label}
              </button>
            </Link>
          );
        })}
      </nav>
      
      <div style={{ padding: '24px', borderTop: '1px solid var(--border-color)', display: 'flex', flexDirection: 'column', gap: '12px', background: 'rgba(0,0,0,0.005)' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>DataHub GMS:</span>
          <span style={{ fontSize: '11px', fontWeight: 600, padding: '2px 8px', borderRadius: '12px', background: 'var(--safe-bg)', color: 'var(--safe)' }}>
            connected
          </span>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>DB Engine:</span>
          <span style={{ fontSize: '11px', fontWeight: 600, padding: '2px 8px', borderRadius: '12px', background: 'var(--safe-bg)', color: 'var(--safe)' }}>
            ready
          </span>
        </div>
      </div>
    </aside>
  );
}
