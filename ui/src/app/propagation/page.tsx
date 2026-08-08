'use client';

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { fetchPropagation } from '@/lib/api';

export default function Propagation() {
  const [data, setData] = useState<any>({ affected_assets: [], paths: [] });

  useEffect(() => {
    async function load() {
      try {
        const res = await fetchPropagation();
        setData(res);
      } catch (err) {
        console.error("Failed to load propagation data", err);
      }
    }
    load();
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '48px', maxWidth: '1400px', margin: '0 auto' }}>
      
      {/* Title Header */}
      <div style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '32px' }}>
        <span style={{ fontSize: '13px', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--accent-indigo)' }}>Lineage Analysis</span>
        <h2 style={{ fontSize: '42px', marginTop: '8px', color: 'var(--text-primary)' }}>Lineage cascade & risk propagation</h2>
        <p style={{ color: 'var(--text-secondary)', marginTop: '8px', fontSize: '15px', maxWidth: '600px', lineHeight: 1.5 }}>
          Downstream risk propagation trace. Unregulated schema drifts or quality drops in upstream datasets recursively infect downstream dependents.
        </p>
      </div>

      <div className="crystalline-surface" style={{ minHeight: '520px', position: 'relative', overflow: 'hidden', padding: '48px', background: 'radial-gradient(circle at 10% 20%, rgba(44, 27, 140, 0.02) 0%, transparent 80%)' }}>
        
        {/* Visual Map Layout */}
        <div style={{ display: 'flex', justifyContent: 'space-around', alignItems: 'center', height: '100%', minHeight: '360px', position: 'relative', zIndex: 10 }}>
          
          {/* Node 1: logging_events (Source) */}
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
            style={{
              width: '140px',
              height: '140px',
              borderRadius: '50%',
              background: '#FAF8F5',
              border: '2.5px solid var(--block)',
              boxShadow: '0 12px 30px rgba(220, 38, 38, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.8)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              zIndex: 20
            }}
          >
            <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-primary)' }}>logging_events</span>
            <span style={{ fontSize: '24px', fontWeight: 700, color: 'var(--block)', margin: '6px 0' }}>33.8</span>
            <span style={{ fontSize: '10px', textTransform: 'uppercase', color: 'var(--text-muted)', letterSpacing: '0.05em', fontWeight: 600 }}>Untrusted</span>
          </motion.div>

          {/* Staggered Edge 1 */}
          <svg style={{ position: 'absolute', left: '26%', width: '220px', height: '60px', zIndex: 5 }}>
            <motion.line
              x1="0"
              y1="30"
              x2="220"
              y2="30"
              stroke="var(--block)"
              strokeWidth="2"
              strokeDasharray="6,6"
              initial={{ pathLength: 0, opacity: 0 }}
              animate={{ pathLength: 1, opacity: 0.4 }}
              transition={{ delay: 0.5, duration: 1 }}
            />
          </svg>

          {/* Node 2: order_details (Dependent) */}
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 0.8, duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
            style={{
              width: '130px',
              height: '130px',
              borderRadius: '50%',
              background: '#FAF8F5',
              border: '2.5px solid var(--caution)',
              boxShadow: '0 12px 30px rgba(217, 119, 6, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.8)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              zIndex: 20
            }}
          >
            <span style={{ fontSize: '13px', fontWeight: 600, color: 'var(--text-primary)' }}>order_details</span>
            <span style={{ fontSize: '22px', fontWeight: 700, color: 'var(--caution)', margin: '4px 0' }}>72.0</span>
            <span style={{ fontSize: '10px', textTransform: 'uppercase', color: 'var(--text-muted)', letterSpacing: '0.05em', fontWeight: 600 }}>Review</span>
            <span style={{ fontSize: '9px', fontWeight: 600, color: 'var(--block)', marginTop: '2px' }}>Penalty: -15.0</span>
          </motion.div>

          {/* Staggered Edge 2 */}
          <svg style={{ position: 'absolute', left: '58%', width: '220px', height: '60px', zIndex: 5 }}>
            <motion.line
              x1="0"
              y1="30"
              x2="220"
              y2="30"
              stroke="var(--block)"
              strokeWidth="2"
              strokeDasharray="6,6"
              initial={{ pathLength: 0, opacity: 0 }}
              animate={{ pathLength: 1, opacity: 0.4 }}
              transition={{ delay: 1.5, duration: 1 }}
            />
          </svg>

          {/* Node 3: daily_sales_summary */}
          <motion.div
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            transition={{ delay: 1.8, duration: 0.6, ease: [0.16, 1, 0.3, 1] }}
            style={{
              width: '120px',
              height: '120px',
              borderRadius: '50%',
              background: '#FAF8F5',
              border: '2.5px solid var(--block)',
              boxShadow: '0 12px 30px rgba(220, 38, 38, 0.08), inset 0 1px 0 rgba(255, 255, 255, 0.8)',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              zIndex: 20
            }}
          >
            <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-primary)' }}>daily_sales</span>
            <span style={{ fontSize: '20px', fontWeight: 700, color: 'var(--block)', margin: '2px 0' }}>52.4</span>
            <span style={{ fontSize: '9px', textTransform: 'uppercase', color: 'var(--text-muted)', letterSpacing: '0.05em', fontWeight: 600 }}>Untrusted</span>
            <span style={{ fontSize: '9px', fontWeight: 600, color: 'var(--block)' }}>Penalty: -10.5</span>
          </motion.div>

        </div>

        {/* Legend */}
        <div style={{ display: 'flex', gap: '32px', justifyContent: 'center', marginTop: '48px', borderTop: '1px solid var(--border-color)', paddingTop: '32px' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px', color: 'var(--text-secondary)' }}>
            <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: 'var(--block)' }}></span> Untrusted (Score &lt; 55)
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px', color: 'var(--text-secondary)' }}>
            <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: 'var(--caution)' }}></span> Review (Score 55 - 74)
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', fontSize: '13px', color: 'var(--text-secondary)' }}>
            <span style={{ width: '10px', height: '10px', borderRadius: '50%', background: 'var(--safe)' }}></span> Trusted (Score &gt;= 75)
          </div>
        </div>

      </div>
    </div>
  );
}
