'use client';

import { useState, useRef } from 'react';
import { ShieldAlert, ShieldCheck } from 'lucide-react';
import { getApiUrl } from '@/lib/api';

export default function MLGate() {
  const [urnInput, setUrnInput] = useState('urn:li:dataset:(urn:li:dataPlatform:dbt,b2fd91.ORDER_ENTRY_DB.analytics.order_details,PROD)\nurn:li:dataset:(urn:li:dataPlatform:hive,logging_events,PROD)');
  const [verdict, setVerdict] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  // Proximity highlight card tracking
  const cardRefLeft = useRef<HTMLDivElement>(null);
  const cardRefRight = useRef<HTMLDivElement>(null);

  const checkMLGate = async () => {
    setLoading(true);
    const urns = urnInput.split('\n').map(u => u.trim()).filter(Boolean);
    try {
      let url = getApiUrl('/ml');
      let res;
      try {
        res = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(urns)
        });
        if (!res.ok) throw new Error();
      } catch (err) {
        console.warn("Backend ML gate connection failed. Falling back to Next.js mock API...", err);
        res = await fetch('/api/ml', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(urns)
        });
      }
      const data = await res.json();
      setVerdict(data);
    } catch (e) {
      console.error("ML Gate request failed", e);
    } finally {
      setLoading(false);
    }
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>, ref: React.RefObject<HTMLDivElement>) => {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    ref.current.style.setProperty('--mouse-x', `${x}px`);
    ref.current.style.setProperty('--mouse-y', `${y}px`);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '48px', maxWidth: '1200px', margin: '0 auto' }}>
      
      {/* Page Header */}
      <div style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '32px' }}>
        <span style={{ fontSize: '13px', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--accent-indigo)' }}>Integrity Guard</span>
        <h2 style={{ fontSize: '42px', marginTop: '8px', color: 'var(--text-primary)' }}>ML ingestion & training gate</h2>
        <p style={{ color: 'var(--text-secondary)', marginTop: '8px', fontSize: '15px', maxWidth: '600px', lineHeight: 1.5 }}>
          Verify target training datasets and all upstream lineage paths before execution runs. Proactively block corrupt data sources.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
        
        {/* Left Side: Input Form */}
        <div
          ref={cardRefLeft}
          onMouseMove={(e) => handleMouseMove(e, cardRefLeft)}
          className="crystalline-surface"
          style={{ position: 'relative', overflow: 'hidden', display: 'flex', flexDirection: 'column', gap: '24px' }}
        >
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            pointerEvents: 'none',
            background: 'radial-gradient(180px circle at var(--mouse-x, 0px) var(--mouse-y, 0px), rgba(44, 27, 140, 0.05), transparent)'
          }} />
          <h3 style={{ fontSize: '20px', fontWeight: 500 }}>Training Source URNs</h3>
          <textarea
            value={urnInput}
            onChange={(e) => setUrnInput(e.target.value)}
            style={{
              width: '100%',
              height: '200px',
              background: '#FAF8F5',
              border: '1px solid var(--border-color)',
              borderRadius: '8px',
              padding: '20px',
              color: 'var(--text-primary)',
              fontFamily: 'var(--font-mono)',
              fontSize: '13px',
              lineHeight: 1.6,
              resize: 'none',
              boxShadow: 'inset 0 2px 8px rgba(0,0,0,0.015)',
              position: 'relative',
              zIndex: 10
            }}
            placeholder="Enter DataHub URNs, one per line..."
          />
          <button
            onClick={checkMLGate}
            disabled={loading}
            className="btn-luxury btn-luxury-primary"
            style={{ padding: '14px', fontSize: '14px', width: '100%', textAlign: 'center', position: 'relative', zIndex: 10 }}
          >
            {loading ? 'Analyzing Lineage Graph...' : 'Verify Training Safety'}
          </button>
        </div>

        {/* Right Side: Verification Verdicts */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
          {verdict ? (
            <div
              ref={cardRefRight}
              onMouseMove={(e) => handleMouseMove(e, cardRefRight)}
              className="crystalline-surface"
              style={{
                position: 'relative',
                overflow: 'hidden',
                border: verdict.verdict === 'BLOCK_TRAINING' ? '1px solid var(--block)' : verdict.verdict === 'CAUTION' ? '1px solid var(--caution)' : '1px solid var(--safe)',
                background: verdict.verdict === 'BLOCK_TRAINING' ? 'rgba(220, 38, 38, 0.02)' : verdict.verdict === 'CAUTION' ? 'rgba(217, 119, 6, 0.02)' : 'rgba(16, 133, 88, 0.02)',
                display: 'flex',
                flexDirection: 'column',
                gap: '24px'
              }}
            >
              <div style={{
                position: 'absolute',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                pointerEvents: 'none',
                background: 'radial-gradient(180px circle at var(--mouse-x, 0px) var(--mouse-y, 0px), rgba(44, 27, 140, 0.05), transparent)'
              }} />
              <div style={{ display: 'flex', alignItems: 'center', gap: '16px', position: 'relative', zIndex: 10 }}>
                {verdict.verdict === 'BLOCK_TRAINING' ? (
                  <ShieldAlert size={36} color="var(--block)" />
                ) : (
                  <ShieldCheck size={36} color="var(--safe)" />
                )}
                <div>
                  <h4 style={{ fontSize: '20px', fontWeight: 600, color: verdict.verdict === 'BLOCK_TRAINING' ? 'var(--block)' : verdict.verdict === 'CAUTION' ? 'var(--caution)' : 'var(--safe)' }}>
                    {verdict.verdict}
                  </h4>
                  <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Verdict Status</span>
                </div>
              </div>

              <p style={{ fontSize: '15px', lineHeight: 1.6, color: 'var(--text-primary)', fontStyle: 'italic', position: 'relative', zIndex: 10 }}>
                "{verdict.summary}"
              </p>
              
              <div style={{ padding: '20px', background: 'rgba(0,0,0,0.005)', borderRadius: '8px', border: '1px solid var(--border-color)', position: 'relative', zIndex: 10 }}>
                <span style={{ fontSize: '11px', fontWeight: 600, textTransform: 'uppercase', color: 'var(--text-muted)', display: 'block', marginBottom: '6px' }}>Recommendation</span>
                <p style={{ fontSize: '14px', fontWeight: 600, color: 'var(--text-primary)' }}>{verdict.recommendation}</p>
              </div>

              {verdict.upstream_risks?.length > 0 && (
                <div style={{ marginTop: '12px', position: 'relative', zIndex: 10 }}>
                  <h5 style={{ fontSize: '12px', fontWeight: 600, textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: '12px', borderBottom: '1px solid var(--border-color)', paddingBottom: '8px' }}>
                    Upstream Lineage Gaps Found
                  </h5>
                  {verdict.upstream_risks.map((risk: any, idx: number) => (
                    <div key={idx} style={{ padding: '12px 0', borderBottom: '1px solid var(--border-color)', fontSize: '13px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div>
                        <span style={{ fontWeight: 600, color: 'var(--text-primary)', fontFamily: 'var(--font-mono)' }}>{risk.name}</span>
                        <p style={{ fontSize: '12px', color: 'var(--text-muted)', marginTop: '2px' }}>{risk.reason}</p>
                      </div>
                      <span style={{ fontWeight: 700, color: 'var(--block)' }}>{risk.score}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <div className="crystalline-surface" style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '100%', minHeight: '320px', textAlign: 'center' }}>
              <p style={{ color: 'var(--text-secondary)', fontSize: '15px' }}>Enter URNs and run safety checks to evaluate dataset readiness.</p>
            </div>
          )}
        </div>

      </div>
    </div>
  );
}
