'use client';

import { useState, useEffect } from 'react';
import { fetchDigests } from '@/lib/api';

export default function Assessments() {
  const [digests, setDigests] = useState<any[]>([]);
  const [selectedDigest, setSelectedDigest] = useState<any>(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchDigests();
        setDigests(data);
        if (data.length > 0) setSelectedDigest(data[0]);
      } catch (err) {
        console.error("Failed to load digests", err);
      }
    }
    load();
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '48px', maxWidth: '1400px', margin: '0 auto' }}>
      
      {/* Page Header */}
      <div style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '32px' }}>
        <span style={{ fontSize: '13px', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--accent-indigo)' }}>Chronicles</span>
        <h2 style={{ fontSize: '42px', marginTop: '8px', color: 'var(--text-primary)' }}>Daily digests & intelligence history</h2>
        <p style={{ color: 'var(--text-secondary)', marginTop: '8px', fontSize: '15px', maxWidth: '600px', lineHeight: 1.5 }}>
          Chronological audits of catalog metadata. Natural language summaries and delta reports generated dynamically after each run.
        </p>
      </div>

      <div style={{ display: 'flex', gap: '32px' }}>
        
        {/* Left Side: Digests list */}
        <div style={{ width: '360px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {digests.map(d => (
            <div
              key={d.run_id}
              onClick={() => setSelectedDigest(d)}
              className="crystalline-surface"
              style={{
                cursor: 'pointer',
                padding: '24px',
                border: selectedDigest?.run_id === d.run_id ? '1px solid var(--primary)' : '1px solid var(--border-color)',
                background: selectedDigest?.run_id === d.run_id ? 'rgba(44, 27, 140, 0.04)' : 'var(--bg-glass-primary)',
                transition: 'all 0.4s cubic-bezier(0.16, 1, 0.3, 1)'
              }}
            >
              <h4 style={{ fontSize: '16px', fontWeight: 600 }}>{d.title}</h4>
              <span style={{
                fontSize: '11px',
                color: 'var(--text-muted)',
                display: 'block',
                marginTop: '12px',
                fontFamily: 'var(--font-mono)'
              }}>
                Run: {d.run_id}
              </span>
            </div>
          ))}
        </div>

        {/* Right Side: Digest details */}
        {selectedDigest ? (
          <div className="crystalline-surface" style={{ flex: 1, padding: '48px', display: 'flex', flexDirection: 'column', gap: '32px' }}>
            <h3 style={{ fontSize: '28px', fontWeight: 500, borderBottom: '1px solid var(--border-color)', paddingBottom: '20px' }}>
              {selectedDigest.title}
            </h3>
            
            <div style={{
              background: '#FAF8F5',
              padding: '40px',
              borderRadius: '8px',
              border: '1px solid var(--border-color)',
              color: 'var(--text-primary)',
              lineHeight: 1.7,
              fontSize: '15px',
              fontFamily: 'var(--font-sans)',
              boxShadow: 'inset 0 2px 8px rgba(0,0,0,0.01)'
            }}>
              <h4 style={{ fontSize: '14px', fontWeight: 600, color: 'var(--accent-indigo)', marginBottom: '20px', letterSpacing: '0.05em', textTransform: 'uppercase' }}>
                PRAXIS Assessment Run Summary
              </h4>
              <p style={{ marginBottom: '20px' }}>
                During today's continuous intelligence scan, the Census Agent inventoried 52 active metadata datasets across 4 core organizational business domains.
              </p>
              
              <h4 style={{ fontSize: '15px', fontWeight: 600, marginTop: '24px', marginBottom: '12px', color: 'var(--text-primary)' }}>Key Findings:</h4>
              <ul style={{ paddingLeft: '20px', display: 'flex', flexDirection: 'column', gap: '12px', color: 'var(--text-secondary)' }}>
                <li><strong>Logistics Domain</strong> remains at a low trust rating (D grade, average score 58.0) due to extensive missing owners and descriptions on Hive schemas.</li>
                <li><strong>Lineage Contagion</strong> was traced: <code>logging_events</code> failure (score 33.8) propagated score drops to downstream consumers, including <code>order_details</code>.</li>
                <li><strong>Remediations Deployed:</strong> Compiled 2 new validation configurations and data contracts, and opened remediation branches on Git.</li>
              </ul>
            </div>
          </div>
        ) : (
          <div className="crystalline-surface" style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '400px' }}>
            <span style={{ color: 'var(--text-muted)' }}>Select an assessment run to view details.</span>
          </div>
        )}

      </div>
    </div>
  );
}
