'use client';

import { useState, useEffect } from 'react';
import { fetchContracts } from '@/lib/api';

export default function Contracts() {
  const [contracts, setContracts] = useState<any[]>([]);
  const [selectedContract, setSelectedContract] = useState<any>(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchContracts();
        setContracts(data);
        if (data.length > 0) setSelectedContract(data[0]);
      } catch (err) {
        console.error("Failed to load contracts", err);
      }
    }
    load();
  }, []);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '48px', maxWidth: '1400px', margin: '0 auto' }}>
      
      {/* Title Header */}
      <div style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '32px' }}>
        <span style={{ fontSize: '13px', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.1em', color: 'var(--accent-indigo)' }}>Remediation Suite</span>
        <h2 style={{ fontSize: '42px', marginTop: '8px', color: 'var(--text-primary)' }}>Synthesized code & contracts</h2>
        <p style={{ color: 'var(--text-secondary)', marginTop: '8px', fontSize: '15px', maxWidth: '600px', lineHeight: 1.5 }}>
          Automatically synthesized schema tests, SQL assertions, and documentation to restore trust parameter health for low-scoring assets.
        </p>
      </div>

      <div style={{ display: 'flex', gap: '32px' }}>
        
        {/* Left Side: Contracts list */}
        <div style={{ width: '360px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          {contracts.map(c => (
            <div
              key={c.id}
              onClick={() => setSelectedContract(c)}
              className="crystalline-surface"
              style={{
                cursor: 'pointer',
                padding: '24px',
                border: selectedContract?.id === c.id ? '1px solid var(--primary)' : '1px solid var(--border-color)',
                background: selectedContract?.id === c.id ? 'rgba(44, 27, 140, 0.04)' : 'var(--bg-glass-primary)',
                transition: 'all 0.4s cubic-bezier(0.16, 1, 0.3, 1)'
              }}
            >
              <h4 style={{ fontSize: '15px', fontWeight: 600, fontFamily: 'var(--font-mono)' }}>{c.filename}</h4>
              <span style={{
                fontSize: '11px',
                textTransform: 'uppercase',
                color: 'var(--text-muted)',
                display: 'inline-block',
                marginTop: '12px',
                letterSpacing: '0.05em',
                fontWeight: 600
              }}>
                Artifact: {c.artifact_type.replace('_', ' ')}
              </span>
            </div>
          ))}
        </div>

        {/* Right Side: Contract detail & viewer */}
        {selectedContract ? (
          <div className="crystalline-surface" style={{ flex: 1, padding: '40px', display: 'flex', flexDirection: 'column', gap: '32px' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
              <div>
                <h3 style={{ fontSize: '24px', fontWeight: 500, fontFamily: 'var(--font-mono)' }}>{selectedContract.filename}</h3>
                <span style={{ fontSize: '13px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)', display: 'block', marginTop: '6px', wordBreak: 'break-all' }}>
                  Target: {selectedContract.target_urn}
                </span>
              </div>
              <button
                onClick={() => {
                  const blob = new Blob([selectedContract.content], { type: 'text/yaml' });
                  const url = URL.createObjectURL(blob);
                  const a = document.createElement('a');
                  a.href = url;
                  a.download = selectedContract.filename;
                  a.click();
                }}
                className="btn-luxury btn-luxury-primary"
                style={{ padding: '12px 24px', fontSize: '13px' }}
              >
                Download Code
              </button>
            </div>

            <div style={{ background: 'rgba(0,0,0,0.005)', padding: '24px', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
              <h5 style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '12px' }}>Grounding Evidence</h5>
              <ul style={{ paddingLeft: '20px', fontSize: '14px', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '8px', lineHeight: 1.5 }}>
                {selectedContract.grounding_evidence?.map((e: string, idx: number) => (
                  <li key={idx}>{e}</li>
                ))}
              </ul>
            </div>

            <pre style={{
              background: '#FAF8F5',
              padding: '32px',
              borderRadius: '8px',
              border: '1px solid var(--border-color)',
              color: 'var(--accent-indigo)',
              fontFamily: 'var(--font-mono)',
              fontSize: '13px',
              lineHeight: 1.7,
              overflowX: 'auto',
              whiteSpace: 'pre-wrap',
              boxShadow: 'inset 0 2px 8px rgba(0,0,0,0.015)'
            }}>
              {selectedContract.content}
            </pre>
          </div>
        ) : (
          <div className="crystalline-surface" style={{ flex: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '400px' }}>
            <span style={{ color: 'var(--text-muted)' }}>No synthesized artifacts available.</span>
          </div>
        )}

      </div>
    </div>
  );
}
