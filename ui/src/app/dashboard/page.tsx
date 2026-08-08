'use client';

import { useState, useEffect, useRef } from 'react';
import Link from 'next/link';
import { fetchCatalog, fetchAssets, fetchDomains } from '@/lib/api';
import { BarChart2, ShieldCheck, Cpu, RefreshCw } from 'lucide-react';

export default function Dashboard() {
  const [catalog, setCatalog] = useState<any>({ total_datasets: 0, grade_distribution: {}, tier_distribution: {} });
  const [assets, setAssets] = useState<any[]>([]);
  const [domains, setDomains] = useState<any[]>([]);
  const [selectedAsset, setSelectedAsset] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  // Canvas visualizer reference
  const visualizationCanvasRef = useRef<HTMLCanvasElement>(null);

  // Proximity highlight card tracking
  const metricsCardRef1 = useRef<HTMLDivElement>(null);
  const metricsCardRef2 = useRef<HTMLDivElement>(null);
  const metricsCardRef3 = useRef<HTMLDivElement>(null);

  useEffect(() => {
    async function load() {
      try {
        const cat = await fetchCatalog();
        const ast = await fetchAssets();
        const dom = await fetchDomains();
        setCatalog(cat);
        setAssets(ast);
        setDomains(dom);
        if (ast.length > 0) setSelectedAsset(ast[0]);
      } catch (err) {
        console.error("Failed to load catalog data", err);
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  // Scientific Trust Network Constellation Animation
  useEffect(() => {
    const canvas = visualizationCanvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let width = (canvas.width = canvas.parentElement?.clientWidth || 600);
    let height = (canvas.height = 360);

    const handleResize = () => {
      width = canvas.width = canvas.parentElement?.clientWidth || 600;
      height = canvas.height = 360;
    };
    window.addEventListener('resize', handleResize);

    // Create stable random node coordinates representing data catalogs
    const nodes: any[] = [];
    const numNodes = 18;
    for (let i = 0; i < numNodes; i++) {
      nodes.push({
        x: Math.random() * width,
        y: Math.random() * height,
        vx: (Math.random() - 0.5) * 0.4,
        vy: (Math.random() - 0.5) * 0.4,
        radius: Math.random() * 4 + 5,
        color: Math.random() > 0.7 ? 'rgba(44, 27, 140, 0.75)' : 'rgba(13, 99, 214, 0.75)'
      });
    }

    let animationFrameId: number;

    const render = () => {
      ctx.clearRect(0, 0, width, height);

      // Draw soft grid background alignment lines
      ctx.strokeStyle = 'rgba(29, 29, 31, 0.015)';
      ctx.lineWidth = 1;
      for (let x = 0; x < width; x += 40) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
      }

      // Draw lineage paths / connection wires between nodes
      ctx.strokeStyle = 'rgba(29, 29, 31, 0.085)';
      ctx.lineWidth = 1.2;
      for (let i = 0; i < numNodes; i++) {
        for (let j = i + 1; j < numNodes; j++) {
          const dx = nodes[i].x - nodes[j].x;
          const dy = nodes[i].y - nodes[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);

          if (dist < 140) {
            ctx.beginPath();
            ctx.moveTo(nodes[i].x, nodes[i].y);
            ctx.lineTo(nodes[j].x, nodes[j].y);
            ctx.stroke();
          }
        }
      }

      // Draw data nodes
      nodes.forEach(node => {
        ctx.beginPath();
        ctx.arc(node.x, node.y, node.radius, 0, Math.PI * 2);
        ctx.fillStyle = node.color;
        ctx.fill();

        // Slow motion update
        node.x += node.vx;
        node.y += node.vy;

        // Bounce boundaries
        if (node.x < 0 || node.x > width) node.vx *= -1;
        if (node.y < 0 || node.y > height) node.vy *= -1;
      });

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      window.removeEventListener('resize', handleResize);
      cancelAnimationFrame(animationFrameId);
    };
  }, [loading]);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>, ref: React.RefObject<HTMLDivElement>) => {
    if (!ref.current) return;
    const rect = ref.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    ref.current.style.setProperty('--mouse-x', `${x}px`);
    ref.current.style.setProperty('--mouse-y', `${y}px`);
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '56px', maxWidth: '1440px', margin: '0 auto', width: '100%' }}>
      
      {/* 1. COMMAND SYSTEM HERO */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(12, 1fr)',
        gap: '40px',
        borderBottom: '1px solid var(--border-color)',
        paddingBottom: '48px',
        alignItems: 'center'
      }}>
        <div style={{ gridColumn: 'span 7' }}>
          <span style={{ fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.15em', color: 'var(--accent-indigo)' }}>
            PRAXIS / OPERATIONAL CENTER
          </span>
          <h2 style={{ fontSize: '56px', marginTop: '16px', fontWeight: 300, lineHeight: 1.05 }}>
            TRUST <br />
            INTELLIGENCE <br />
            OVERVIEW
          </h2>
          <p style={{ color: 'var(--text-secondary)', marginTop: '24px', fontSize: '15px', maxWidth: '440px', lineHeight: 1.5 }}>
            Central metadata pipeline registry. Real-time trust scoring and automatic downstream risk propagation.
          </p>
        </div>

        {/* Crystalline Scientific Instrument Visual Widget */}
        <div className="crystalline-surface" style={{ gridColumn: 'span 5', padding: 0, overflow: 'hidden', height: '360px', position: 'relative' }}>
          <canvas ref={visualizationCanvasRef} style={{ width: '100%', height: '100%' }} />
          <div style={{
            position: 'absolute',
            top: '20px',
            left: '20px',
            fontSize: '11px',
            fontFamily: 'var(--font-mono)',
            color: 'var(--text-muted)'
          }}>
            [ LIVE CONSTELLATION GRAPH ]
          </div>
        </div>
      </div>

      {/* 2. COMMAND TELEMETRY STATS - Luminous objects */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '32px' }}>
        
        {/* Metric 1 */}
        <div
          ref={metricsCardRef1}
          onMouseMove={(e) => handleMouseMove(e, metricsCardRef1)}
          className="crystalline-surface"
          style={{ position: 'relative', overflow: 'hidden', display: 'flex', flexDirection: 'column', gap: '16px', padding: '40px' }}
        >
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            pointerEvents: 'none',
            background: 'radial-gradient(200px circle at var(--mouse-x, 0px) var(--mouse-y, 0px), rgba(44, 27, 140, 0.05), transparent)'
          }} />
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>Assessed Datasets</span>
            <BarChart2 size={15} color="var(--accent-indigo)" />
          </div>
          <h3 style={{ fontSize: '72px', fontWeight: 300, fontFamily: 'var(--font-serif)', lineHeight: 1 }}>
            {catalog.total_datasets || 52}
          </h3>
          <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Full metadata schemas audited</span>
        </div>

        {/* Metric 2 */}
        <div
          ref={metricsCardRef2}
          onMouseMove={(e) => handleMouseMove(e, metricsCardRef2)}
          className="crystalline-surface"
          style={{ position: 'relative', overflow: 'hidden', display: 'flex', flexDirection: 'column', gap: '16px', padding: '40px' }}
        >
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            pointerEvents: 'none',
            background: 'radial-gradient(200px circle at var(--mouse-x, 0px) var(--mouse-y, 0px), rgba(44, 27, 140, 0.05), transparent)'
          }} />
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>Downstream Risks</span>
            <Cpu size={15} color="var(--accent-indigo)" />
          </div>
          <h3 style={{ fontSize: '72px', fontWeight: 300, fontFamily: 'var(--font-serif)', lineHeight: 1 }}>
            12
          </h3>
          <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>Quality penalties propagated downstream</span>
        </div>

        {/* Metric 3 */}
        <div
          ref={metricsCardRef3}
          onMouseMove={(e) => handleMouseMove(e, metricsCardRef3)}
          className="crystalline-surface"
          style={{ position: 'relative', overflow: 'hidden', display: 'flex', flexDirection: 'column', gap: '16px', padding: '40px' }}
        >
          <div style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            pointerEvents: 'none',
            background: 'radial-gradient(200px circle at var(--mouse-x, 0px) var(--mouse-y, 0px), rgba(44, 27, 140, 0.05), transparent)'
          }} />
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.05em', color: 'var(--text-muted)' }}>Remediations</span>
            <ShieldCheck size={15} color="var(--accent-indigo)" />
          </div>
          <h3 style={{ fontSize: '72px', fontWeight: 300, fontFamily: 'var(--font-serif)', lineHeight: 1 }}>
            335
          </h3>
          <span style={{ fontSize: '13px', color: 'var(--text-secondary)' }}>dbt schemas and data contracts pushed</span>
        </div>

      </div>

      {/* 3. OPERATIONAL DETAILS PANEL SPLIT */}
      <div className="editorial-grid">
        
        {/* Left side: Assets Explorer */}
        <div className="crystalline-surface" style={{ gridColumn: 'span 8', padding: 0, overflow: 'hidden' }}>
          <div style={{ padding: '32px 40px', borderBottom: '1px solid var(--border-color)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h3 style={{ fontSize: '24px', fontWeight: 400 }}>Catalog index</h3>
            <span style={{ fontSize: '13px', color: 'var(--text-muted)', fontFamily: 'var(--font-mono)' }}>{assets.length} items logged</span>
          </div>
          
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', fontSize: '14px' }}>
              <thead>
                <tr style={{ borderBottom: '1px solid var(--border-color)', background: 'rgba(0,0,0,0.005)' }}>
                  <th style={{ padding: '20px 40px', color: 'var(--text-secondary)', fontWeight: 600 }}>Asset Name</th>
                  <th style={{ padding: '20px 40px', color: 'var(--text-secondary)', fontWeight: 600 }}>Platform</th>
                  <th style={{ padding: '20px 40px', color: 'var(--text-secondary)', fontWeight: 600, textAlign: 'center' }}>Trust Score</th>
                  <th style={{ padding: '20px 40px', color: 'var(--text-secondary)', fontWeight: 600 }}>Tier</th>
                </tr>
              </thead>
              <tbody>
                {assets.map(asset => (
                  <tr
                    key={asset.urn}
                    onClick={() => setSelectedAsset(asset)}
                    style={{
                      borderBottom: '1px solid var(--border-color)',
                      cursor: 'pointer',
                      background: selectedAsset?.urn === asset.urn ? 'rgba(44, 27, 140, 0.03)' : 'transparent',
                      transition: 'background 0.3s cubic-bezier(0.16, 1, 0.3, 1)'
                    }}
                  >
                    <td style={{ padding: '20px 40px', fontWeight: 600, fontFamily: 'var(--font-mono)' }}>{asset.name}</td>
                    <td style={{ padding: '20px 40px', textTransform: 'capitalize' }}>{asset.platform}</td>
                    <td style={{ padding: '20px 40px', fontWeight: 700, textAlign: 'center', color: asset.composite_score >= 75 ? 'var(--safe)' : asset.composite_score >= 55 ? 'var(--caution)' : 'var(--block)' }}>
                      {asset.composite_score}
                    </td>
                    <td style={{ padding: '20px 40px' }}>
                      <span style={{
                        fontSize: '11px',
                        fontWeight: 700,
                        textTransform: 'uppercase',
                        letterSpacing: '0.05em',
                        padding: '4px 10px',
                        borderRadius: '4px',
                        background: asset.tier === 'trusted' ? 'var(--safe-bg)' : asset.tier === 'review' ? 'var(--caution-bg)' : 'var(--block-bg)',
                        color: asset.tier === 'trusted' ? 'var(--safe)' : asset.tier === 'review' ? 'var(--caution)' : 'var(--block)'
                      }}>
                        {asset.tier}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right side: Detailed Inspection Drawer Panel */}
        <div style={{ gridColumn: 'span 4', display: 'flex', flexDirection: 'column', gap: '32px' }}>
          {selectedAsset ? (
            <div className="crystalline-surface" style={{ display: 'flex', flexDirection: 'column', gap: '28px', padding: '40px' }}>
              <div>
                <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', color: 'var(--accent-indigo)', letterSpacing: '0.05em' }}>Inspection Panel</span>
                <h3 style={{ fontSize: '20px', marginTop: '12px', lineHeight: 1.2, fontFamily: 'var(--font-mono)', wordBreak: 'break-word' }}>{selectedAsset.name}</h3>
                <span style={{ fontSize: '12px', color: 'var(--text-muted)', display: 'block', marginTop: '6px' }}>{selectedAsset.platform.toUpperCase()}</span>
              </div>

              <div style={{ borderTop: '1px solid var(--border-color)', paddingTop: '20px' }}>
                <span style={{ fontSize: '12px', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>Audited Verdict Summary</span>
                <p style={{ fontSize: '14px', lineHeight: 1.6, color: 'var(--text-secondary)', marginTop: '8px', fontStyle: 'italic' }}>
                  "{selectedAsset.evidence_summary || 'No summary generated.'}"
                </p>
              </div>

              {/* Dimensions list */}
              <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                {Object.entries(selectedAsset.dimensions || {}).map(([dimName, dim]: any) => (
                  <div key={dimName} style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px' }}>
                      <span style={{ fontWeight: 500, textTransform: 'capitalize' }}>{dimName}</span>
                      <span style={{ fontWeight: 700, color: dim.score >= 75 ? 'var(--safe)' : dim.score >= 55 ? 'var(--caution)' : 'var(--block)' }}>{dim.score}/100</span>
                    </div>
                    <div style={{ height: '4px', background: 'var(--bg-mist-grey)', borderRadius: '2px', overflow: 'hidden' }}>
                      <div style={{
                        height: '100%',
                        width: `${dim.score}%`,
                        background: dim.score >= 75 ? 'var(--safe)' : dim.score >= 55 ? 'var(--caution)' : 'var(--block)',
                        borderRadius: '2px'
                      }} />
                    </div>
                  </div>
                ))}
              </div>

              <Link href={`/assets/${encodeURIComponent(selectedAsset.urn)}`} className="btn-luxury btn-luxury-primary" style={{ textAlign: 'center', marginTop: '12px' }}>
                Inspect deep lineage & code
              </Link>
            </div>
          ) : (
            <div className="crystalline-surface" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', minHeight: '300px' }}>
              <span style={{ color: 'var(--text-muted)' }}>Select an asset to view dimensions</span>
            </div>
          )}
        </div>

      </div>

    </div>
  );
}
