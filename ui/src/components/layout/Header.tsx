'use client';

import { useState } from 'react';
import { Play } from 'lucide-react';

export default function Header() {
  const isDemoMode = process.env.NEXT_PUBLIC_MODE === 'fixture';
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState(0);

  const triggerRun = async () => {
    setIsRunning(true);
    setProgress(20);
    setTimeout(() => setProgress(50), 1000);
    setTimeout(() => setProgress(80), 2000);
    setTimeout(() => {
      setProgress(100);
      setIsRunning(false);
    }, 3000);
  };

  return (
    <header style={{
      padding: '24px 40px',
      borderBottom: '1px solid var(--border-color)',
      background: 'rgba(250, 248, 245, 0.65)',
      backdropFilter: 'blur(20px)',
      WebkitBackdropFilter: 'blur(20px)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'space-between',
      position: 'sticky',
      top: 0,
      zIndex: 90
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
        <span style={{ fontSize: '13px', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>Workspace</span>
        {isDemoMode && (
          <span style={{
            fontSize: '11px',
            fontWeight: 700,
            padding: '4px 12px',
            borderRadius: '12px',
            background: 'var(--caution-bg)',
            color: 'var(--caution)',
            border: '1px solid rgba(217, 119, 6, 0.3)'
          }}>
            DEMO MODE (FIXTURES)
          </span>
        )}
      </div>

      <div style={{ display: 'flex', alignItems: 'center', gap: '20px' }}>
        {isRunning && (
          <div style={{ width: '120px', height: '6px', background: 'var(--bg-mist-grey)', borderRadius: '3px', overflow: 'hidden' }}>
            <div style={{ width: `${progress}%`, height: '100%', background: 'var(--primary)', transition: 'width 0.4s ease' }}></div>
          </div>
        )}
        <button
          onClick={triggerRun}
          disabled={isRunning}
          style={{
            padding: '10px 20px',
            borderRadius: '100px',
            border: 'none',
            background: isRunning ? 'var(--bg-mist-grey)' : 'var(--primary)',
            color: isRunning ? 'var(--text-secondary)' : '#faf8f5',
            fontWeight: 500,
            fontSize: '13px',
            cursor: isRunning ? 'not-allowed' : 'pointer',
            display: 'flex',
            alignItems: 'center',
            gap: '8px',
            boxShadow: isRunning ? 'none' : '0 4px 12px rgba(44, 27, 140, 0.15)',
            transition: 'all 0.3s cubic-bezier(0.16, 1, 0.3, 1)'
          }}
        >
          <Play size={12} fill={isRunning ? "none" : "#faf8f5"} />
          Trigger Audit
        </button>
      </div>
    </header>
  );
}
