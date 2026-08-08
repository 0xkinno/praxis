'use client';

import { useState, useEffect } from 'react';
import { fetchAssets } from '@/lib/api';
import { TrustScore } from '@/lib/types';
import Link from 'next/link';

export default function AssetDetail({ params }: { params: { urn: string } }) {
  const decodedUrn = decodeURIComponent(params.urn);
  const [asset, setAsset] = useState<TrustScore | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      try {
        const all = await fetchAssets();
        const match = all.find((a: any) => a.urn === decodedUrn);
        setAsset(match || null);
      } catch (err) {
        console.error("Failed to load asset details", err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, [decodedUrn]);

  if (loading) {
    return (
      <div className="crystalline-surface" style={{ padding: '80px', textAlign: 'center', maxWidth: '800px', margin: '40px auto' }}>
        <h3 style={{ fontSize: '24px', fontWeight: 500 }}>Loading asset metadata...</h3>
        <p style={{ color: 'var(--text-secondary)', marginTop: '12px' }}>Reading from DataHub GMS & local database...</p>
      </div>
    );
  }

  if (!asset) {
    return (
      <div className="crystalline-surface" style={{ padding: '80px', textAlign: 'center', maxWidth: '800px', margin: '40px auto' }}>
        <h3 style={{ fontSize: '24px', fontWeight: 500, color: 'var(--block)' }}>Asset URN not found</h3>
        <p style={{ color: 'var(--text-secondary)', marginTop: '12px' }}>Verify the URN exists in the catalog or search indexes.</p>
        <Link href="/dashboard" className="btn-luxury btn-luxury-primary" style={{ marginTop: '24px' }}>
          Back to Dashboard
        </Link>
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '48px', maxWidth: '1400px', margin: '0 auto' }}>
      
      {/* Detail Header */}
      <div style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '32px' }}>
        <Link href="/dashboard" style={{ color: 'var(--accent-indigo)', textDecoration: 'none', fontSize: '14px', fontWeight: 600, display: 'inline-flex', alignItems: 'center', gap: '8px' }}>
          &larr; Back to Catalog Overview
        </Link>
        <h2 style={{ fontSize: '42px', marginTop: '16px', color: 'var(--text-primary)', fontFamily: 'var(--font-mono)', wordBreak: 'break-all' }}>{asset.name}</h2>
        <span style={{ fontSize: '13px', fontFamily: 'var(--font-mono)', color: 'var(--text-muted)', display: 'block', marginTop: '8px', wordBreak: 'break-all' }}>
          {asset.urn}
        </span>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '360px 1fr', gap: '32px' }}>
        
        {/* Left Side: Score & Tier card */}
        <div className="crystalline-surface" style={{ display: 'flex', flexDirection: 'column', gap: '32px', height: 'fit-content', padding: '40px' }}>
          <div>
            <span style={{ fontSize: '12px', fontWeight: 600, textTransform: 'uppercase', color: 'var(--text-muted)' }}>Compliance Verdict</span>
          </div>
          
          <div style={{ display: 'flex', alignItems: 'center', gap: '24px' }}>
            <div style={{
              width: '90px',
              height: '90px',
              borderRadius: '50%',
              background: 'var(--primary-glow)',
              border: '2.5px solid var(--primary)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: '32px',
              fontWeight: 700,
              color: 'var(--text-primary)'
            }}>
              {asset.composite_score}
            </div>
            <div>
              <div style={{ fontSize: '18px', fontWeight: 700, color: 'var(--text-primary)' }}>Grade: {asset.grade}</div>
              <div style={{ fontSize: '13px', color: 'var(--text-secondary)', textTransform: 'capitalize', marginTop: '2px' }}>Tier: {asset.tier}</div>
            </div>
          </div>
          
          <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '20px' }}>
            <span style={{ fontSize: '12px', fontWeight: 600, textTransform: 'uppercase', color: 'var(--text-muted)', display: 'block', marginBottom: '8px' }}>Prose Summary</span>
            <p style={{ fontSize: '14px', color: 'var(--text-secondary)', lineHeight: 1.6, fontStyle: 'italic' }}>
              "{asset.evidence_summary || 'No prose summary available.'}"
            </p>
          </div>
        </div>

        {/* Right Side: Dimension breakdown */}
        <div className="crystalline-surface" style={{ display: 'flex', flexDirection: 'column', gap: '32px', padding: '40px' }}>
          <h3 style={{ fontSize: '24px', fontWeight: 500 }}>Dimension audit details</h3>
          
          <div style={{ display: 'flex', flexDirection: 'column', gap: '32px' }}>
            {Object.entries(asset.dimensions).map(([name, dim]: any) => (
              <div key={name} style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '24px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '12px' }}>
                  <h4 style={{ textTransform: 'capitalize', fontWeight: 600, fontSize: '18px', color: 'var(--text-primary)' }}>{name}</h4>
                  <span style={{ fontWeight: 700, color: dim.score >= 75 ? 'var(--safe)' : dim.score >= 55 ? 'var(--caution)' : 'var(--block)' }}>{dim.score}/100</span>
                </div>
                <div style={{ width: '100%', height: '4px', background: 'var(--bg-mist-grey)', borderRadius: '2px', overflow: 'hidden', marginBottom: '16px' }}>
                  <div style={{
                    width: `${dim.score}%`,
                    height: '100%',
                    background: dim.score >= 75 ? 'var(--safe)' : dim.score >= 55 ? 'var(--caution)' : 'var(--block)',
                    borderRadius: '2px'
                  }}></div>
                </div>
                
                <h5 style={{ fontSize: '11px', fontWeight: 600, textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: '8px', letterSpacing: '0.05em' }}>Audited Evidence Logs</h5>
                <ul style={{ paddingLeft: '20px', fontSize: '14px', color: 'var(--text-secondary)', display: 'flex', flexDirection: 'column', gap: '6px', lineHeight: 1.5 }}>
                  {dim.evidence.map((e: string, idx: number) => (
                    <li key={idx}>{e}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>

      </div>
    </div>
  );
}
