'use client';

import { motion } from 'framer-motion';
import { useRef, useState, useEffect } from 'react';
import Link from 'next/link';
import { ShieldCheck, ShieldAlert, CheckCircle, ArrowRight } from 'lucide-react';

// Unified transition easing preset
const transitions = {
  cinematic: { duration: 1.2, ease: [0.16, 1, 0.3, 1] }
};

function ProximityGlowCard({ step, title, desc }: { step: string; title: string; desc: string }) {
  const cardRef = useRef<HTMLDivElement>(null);
  const [isHovered, setIsHovered] = useState(false);

  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (!cardRef.current) return;
    const rect = cardRef.current.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    cardRef.current.style.setProperty('--mouse-x', `${x}px`);
    cardRef.current.style.setProperty('--mouse-y', `${y}px`);
  };

  return (
    <div
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
      className="crystalline-surface"
      style={{
        position: 'relative',
        overflow: 'hidden',
        cursor: 'pointer',
        padding: '48px',
        display: 'flex',
        flexDirection: 'column',
        gap: '24px',
        border: '1px solid var(--border-color)',
        borderRadius: '20px',
        background: 'var(--bg-glass-primary)',
        transform: isHovered ? 'translateY(-6px) scale(1.01)' : 'translateY(0) scale(1)',
        borderColor: isHovered ? 'rgba(44, 27, 140, 0.25)' : 'var(--border-color)',
        transition: 'transform 0.5s cubic-bezier(0.16, 1, 0.3, 1), border-color 0.5s ease',
        boxShadow: isHovered ? '0 30px 70px rgba(44, 27, 140, 0.04)' : 'none'
      }}
    >
      {/* Localized Proximity Radial Light Glow - Behaves like physical light passing through glass */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        pointerEvents: 'none',
        opacity: isHovered ? 1 : 0,
        transition: 'opacity 0.4s ease',
        background: 'radial-gradient(200px circle at var(--mouse-x, 0px) var(--mouse-y, 0px), rgba(44, 27, 140, 0.075), transparent)'
      }} />

      <span style={{ fontSize: '12px', fontWeight: 700, color: 'var(--accent-indigo)', letterSpacing: '0.15em' }}>
        {step}
      </span>
      <h4 style={{ fontSize: '24px', fontWeight: 500, color: 'var(--text-primary)' }}>
        {title}
      </h4>
      <p style={{ fontSize: '14px', lineHeight: 1.6, color: 'var(--text-secondary)' }}>
        {desc}
      </p>
    </div>
  );
}

export default function LandingPage() {
  const [selectedScoreDim, setSelectedScoreDim] = useState('integrity');
  const [pipelineState, setPipelineState] = useState('detect'); // detect, generate, pr

  useEffect(() => {
    const interval = setInterval(() => {
      setPipelineState(prev => {
        if (prev === 'detect') return 'generate';
        if (prev === 'generate') return 'pr';
        return 'detect';
      });
    }, 4500);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ position: 'relative', width: '100%' }}>
      
      <header style={{
        padding: '24px 64px',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        borderBottom: '1px solid var(--border-color)',
        background: '#FAF8F5',
        position: 'sticky',
        top: 0,
        zIndex: 100
      }}>
        <span style={{ fontSize: '20px', fontWeight: 600, letterSpacing: '0.08em', textTransform: 'uppercase' }}>
          PRAXIS
        </span>
        <nav style={{ display: 'flex', gap: '48px', fontSize: '13px', fontWeight: 500, letterSpacing: '0.05em', textTransform: 'uppercase' }}>
          <a href="#about" style={{ color: 'var(--text-secondary)', textDecoration: 'none', transition: 'color 0.3s' }}>About</a>
          <a href="#pipeline" style={{ color: 'var(--text-secondary)', textDecoration: 'none', transition: 'color 0.3s' }}>Pipeline</a>
          <a href="#scoring" style={{ color: 'var(--text-secondary)', textDecoration: 'none', transition: 'color 0.3s' }}>Scoring</a>
          <a href="#cascade" style={{ color: 'var(--text-secondary)', textDecoration: 'none', transition: 'color 0.3s' }}>Cascade</a>
          <a href="#gate" style={{ color: 'var(--text-secondary)', textDecoration: 'none', transition: 'color 0.3s' }}>ML Gate</a>
        </nav>
        <Link href="/dashboard" className="btn-luxury btn-luxury-primary" style={{ padding: '10px 24px', fontSize: '13px' }}>
          Launch Dashboard
        </Link>
      </header>

      {/* 1. HERO SLIDE - Immersive Architectural Split Compositions */}
      <section style={{ minHeight: '85vh', display: 'flex', alignItems: 'center', padding: '64px' }}>
        <div className="editorial-grid" style={{ width: '100%', alignItems: 'center' }}>
          
          {/* Left Column Text */}
          <div style={{ gridColumn: 'span 6', display: 'flex', flexDirection: 'column', gap: '32px', paddingRight: '40px' }}>
            <motion.span
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={transitions.cinematic}
              style={{ fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.2em', color: 'var(--accent-indigo)' }}
            >
              Flagship Trust Intelligence
            </motion.span>
            
            <motion.h1
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ ...transitions.cinematic, delay: 0.1 }}
              style={{ fontSize: '68px', fontWeight: 300, lineHeight: 1.05 }}
            >
              CONTINUOUS <br />
              DATA TRUST <br />
              INTELLIGENCE
            </motion.h1>
            
            <motion.p
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ ...transitions.cinematic, delay: 0.2 }}
              style={{ fontSize: '18px', color: 'var(--text-secondary)', lineHeight: 1.6, maxWidth: '480px' }}
            >
              Transform passive metadata records into dynamic crystalline trust networks. Automatically score, propagate lineage risks, and deploy code-level tests before faults cascade.
            </motion.p>
            
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ ...transitions.cinematic, delay: 0.3 }}
              style={{ display: 'flex', gap: '16px', marginTop: '12px' }}
            >
              <Link href="/dashboard" className="btn-luxury btn-luxury-primary">
                Launch Dashboard
              </Link>
              <a href="#pipeline" className="btn-luxury btn-luxury-secondary">
                Explore Pipeline
              </a>
            </motion.div>
          </div>

          {/* Right Column Photographic bleed visual scene */}
          <div style={{ gridColumn: 'span 6', position: 'relative' }}>
            <motion.div
              initial={{ opacity: 0, scale: 0.97 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ ...transitions.cinematic, duration: 1.5 }}
              style={{
                borderRadius: '24px',
                overflow: 'hidden',
                boxShadow: '0 40px 100px rgba(0, 0, 0, 0.08)',
                border: '1px solid rgba(255, 255, 255, 0.45)',
                aspectRatio: '16/11',
                background: 'var(--bg-glass-secondary)',
                position: 'relative'
              }}
            >
              <img
                src="/images/hero-light-network.jpg"
                alt="Bespoke Crystalline Trust Network"
                style={{ width: '100%', height: '100%', objectFit: 'cover' }}
              />
              <div style={{
                position: 'absolute',
                bottom: '24px',
                right: '24px',
                background: 'rgba(250, 248, 245, 0.85)',
                backdropFilter: 'blur(10px)',
                padding: '12px 20px',
                borderRadius: '8px',
                border: '1px solid var(--border-color)',
                fontSize: '11px',
                fontFamily: 'var(--font-mono)'
              }}>
                SYSTEM VERDICT: VERIFIED TRUST
              </div>
            </motion.div>
          </div>

        </div>
      </section>

      {/* 2. CONCEPT SLIDE - Bold, quiet architectural statements */}
      <section id="about" style={{ padding: '160px 80px', borderTop: '1px solid var(--border-color)', background: 'rgba(0,0,0,0.005)' }}>
        <div style={{ maxWidth: '1100px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '32px' }}>
          <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.15em', color: 'var(--accent-indigo)' }}>Active Metadata Orchestration</span>
          <h2 style={{ fontSize: '56px', fontWeight: 300, lineHeight: 1.15 }}>
            Data compliance decays in silence. <br/>
            PRAXIS mends the lineage loop.
          </h2>
          <p style={{ fontSize: '18px', color: 'var(--text-secondary)', lineHeight: 1.7, maxWidth: '800px', marginTop: '16px' }}>
            Static metadata libraries are archives of historical schema facts. They do not prevent drift. PRAXIS intercept data streams, calculates real-time compliance grades, and implements active safety gates at ingestion.
          </p>
        </div>
      </section>

      {/* 3. MULTI-AGENT METADATA PIPELINE - Architectural glass panels */}
      <section id="pipeline" style={{ padding: '140px 64px', borderTop: '1px solid var(--border-color)' }}>
        <div style={{ width: '100%', maxWidth: '1500px', margin: '0 auto' }}>
          <div style={{ borderBottom: '1px solid var(--border-color)', paddingBottom: '32px', marginBottom: '64px' }}>
            <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', color: 'var(--accent-indigo)', letterSpacing: '0.15em' }}>Operational Pipeline</span>
            <h2 style={{ fontSize: '48px', marginTop: '12px', fontWeight: 300 }}>Multi-agent orchestration</h2>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '32px' }}>
            <ProximityGlowCard
              step="01 / CENSUS"
              title="Catalog Ingestion"
              desc="Actively monitors domains and captures schema structures, column metrics, and description coverage parameters."
            />
            <ProximityGlowCard
              step="02 / ASSESS"
              title="Trust Scoring"
              desc="Evaluates compliance across integrity, provenance, stability, and adoption, producing a composite trust grade."
            />
            <ProximityGlowCard
              step="03 / CASCADE"
              title="Lineage Propagation"
              desc="Recursively maps dependencies to transmit risk factors downstream to all associated pipelines and models."
            />
            <ProximityGlowCard
              step="04 / SHIELD"
              title="Contract Generation"
              desc="Synthesizes dbt testing schemas and data contracts, and commits them via auto-generated pull requests."
            />
          </div>
        </div>
      </section>

      {/* 4. PINNED COMPOSITION - Interactive Trust Scoring Sequence */}
      <section id="scoring" style={{ padding: '140px 64px', borderTop: '1px solid var(--border-color)', background: 'rgba(0,0,0,0.005)' }}>
        <div style={{ width: '100%', maxWidth: '1500px', margin: '0 auto', display: 'grid', gridTemplateColumns: 'repeat(12, 1fr)', gap: '64px' }}>
          
          {/* Left panel selector list */}
          <div style={{ gridColumn: 'span 5', display: 'flex', flexDirection: 'column', gap: '32px' }}>
            <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', color: 'var(--accent-indigo)', letterSpacing: '0.1em' }}>Dimension Parameters</span>
            <h2 style={{ fontSize: '48px', fontWeight: 300 }}>Granular auditing</h2>
            <p style={{ fontSize: '16px', color: 'var(--text-secondary)', lineHeight: 1.6 }}>
              Select an operational dimension to display its calculations, threshold limits, and compliance triggers.
            </p>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '16px' }}>
              {[
                { id: 'integrity', title: '01 / INTEGRITY', desc: 'Evaluates assertion checks and test compliance ratios.' },
                { id: 'provenance', title: '02 / PROVENANCE', desc: 'Checks owner validation and documentation completeness.' },
                { id: 'stability', title: '03 / STABILITY', desc: 'Calculates schema column drifts and type variance.' },
                { id: 'adoption', title: '04 / ADOPTION', desc: 'Measures downstream queries and chart bindings.' }
              ].map(item => (
                <button
                  key={item.id}
                  onClick={() => setSelectedScoreDim(item.id)}
                  style={{
                    padding: '20px',
                    borderRadius: '12px',
                    background: selectedScoreDim === item.id ? 'var(--bg-glass-intel)' : 'transparent',
                    border: '1px solid',
                    borderColor: selectedScoreDim === item.id ? 'var(--border-color)' : 'transparent',
                    textAlign: 'left',
                    cursor: 'pointer',
                    transition: 'all 0.3s cubic-bezier(0.16, 1, 0.3, 1)'
                  }}
                >
                  <h4 style={{ fontSize: '15px', fontWeight: 600, color: selectedScoreDim === item.id ? 'var(--accent-indigo)' : 'var(--text-primary)' }}>{item.title}</h4>
                  <p style={{ fontSize: '13px', color: 'var(--text-secondary)', marginTop: '4px' }}>{item.desc}</p>
                </button>
              ))}
            </div>
          </div>

          {/* Right panel presentation evolving dynamically */}
          <div style={{ gridColumn: 'span 7', display: 'flex', alignItems: 'center' }}>
            <div className="crystalline-surface" style={{ width: '100%', padding: '48px', minHeight: '440px', display: 'flex', flexDirection: 'column', gap: '32px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid var(--border-color)', paddingBottom: '20px' }}>
                <h3 style={{ fontSize: '24px', fontWeight: 500, textTransform: 'capitalize' }}>{selectedScoreDim} score</h3>
                <span style={{ fontSize: '20px', fontWeight: 700, color: 'var(--accent-indigo)' }}>88/100</span>
              </div>

              {selectedScoreDim === 'integrity' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px' }}>
                    <span>Assertions Run</span>
                    <span style={{ fontWeight: 600 }}>50 executed</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px' }}>
                    <span>Pass Success Rate</span>
                    <span style={{ fontWeight: 600, color: 'var(--safe)' }}>98.2% PASSING</span>
                  </div>
                  <div style={{ padding: '16px', background: 'rgba(0,0,0,0.01)', borderRadius: '8px', fontSize: '13px', lineHeight: 1.5, color: 'var(--text-secondary)' }}>
                    "Integrity score monitors assertion test runs and rates. The target dataset successfully resolved 49 out of 50 query test cases."
                  </div>
                </div>
              )}

              {selectedScoreDim === 'provenance' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px' }}>
                    <span>Owners Declared</span>
                    <span style={{ fontWeight: 600, color: 'var(--safe)' }}>VALID</span>
                  </div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px' }}>
                    <span>Glossary Terms</span>
                    <span style={{ fontWeight: 600, color: 'var(--caution)' }}>MISSING TERM REF</span>
                  </div>
                  <div style={{ padding: '16px', background: 'rgba(0,0,0,0.01)', borderRadius: '8px', fontSize: '13px', lineHeight: 1.5, color: 'var(--text-secondary)' }}>
                    "Provenance evaluates documentation coverage. Penalties are issued for empty fields or unassigned tags."
                  </div>
                </div>
              )}

              {selectedScoreDim === 'stability' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px' }}>
                    <span>Schema Drift</span>
                    <span style={{ fontWeight: 600, color: 'var(--safe)' }}>0 CHANGES DETECTED</span>
                  </div>
                  <div style={{ padding: '16px', background: 'rgba(0,0,0,0.01)', borderRadius: '8px', fontSize: '13px', lineHeight: 1.5, color: 'var(--text-secondary)' }}>
                    "Stability measures schema layout updates. Upstream alterations trigger an immediate lineage recalculation warning."
                  </div>
                </div>
              )}

              {selectedScoreDim === 'adoption' && (
                <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '14px' }}>
                    <span>Dependent Systems</span>
                    <span style={{ fontWeight: 600 }}>4 active dashboards</span>
                  </div>
                  <div style={{ padding: '16px', background: 'rgba(0,0,0,0.01)', borderRadius: '8px', fontSize: '13px', lineHeight: 1.5, color: 'var(--text-secondary)' }}>
                    "Adoption tracks frequency of data reads. Datasets bound to active production dashboards carry higher critical tiers."
                  </div>
                </div>
              )}

            </div>
          </div>

        </div>
      </section>

      {/* 5. CASCADE STORY - Left-right image compositions */}
      <section id="cascade" style={{ padding: '140px 64px', borderTop: '1px solid var(--border-color)' }}>
        <div style={{ width: '100%', maxWidth: '1500px', margin: '0 auto', display: 'grid', gridTemplateColumns: 'repeat(12, 1fr)', gap: '64px', alignItems: 'center' }}>
          
          <div style={{ gridColumn: 'span 5', display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', color: 'var(--accent-indigo)', letterSpacing: '0.1em' }}>Lineage Cascades</span>
            <h2 style={{ fontSize: '44px', fontWeight: 300, lineHeight: 1.1 }}>Lineage risk propagation</h2>
            <p style={{ fontSize: '16px', lineHeight: 1.6, color: 'var(--text-secondary)' }}>
              Ingestion decay propagates downstream. A drift warning in an upstream log decodes scores, sending quality warning signals to all downstream analytical nodes.
            </p>
          </div>

          <div style={{ gridColumn: 'span 7' }}>
            <div className="crystalline-surface" style={{ padding: '40px', background: 'var(--bg-glass-secondary)' }}>
              <img
                src="/images/cascade-light.jpg"
                alt="Cascade Lineage Propagation"
                style={{ width: '100%', height: 'auto', borderRadius: '12px', mixBlendMode: 'multiply' }}
              />
            </div>
          </div>

        </div>
      </section>

      {/* 6. ML GATE SLIDE - Split layout */}
      <section id="gate" style={{ padding: '140px 64px', borderTop: '1px solid var(--border-color)', background: 'rgba(0,0,0,0.005)' }}>
        <div style={{ width: '100%', maxWidth: '1500px', margin: '0 auto', display: 'grid', gridTemplateColumns: 'repeat(12, 1fr)', gap: '64px', alignItems: 'center' }}>
          
          <div style={{ gridColumn: 'span 7' }}>
            <div className="crystalline-surface" style={{ padding: '40px', background: 'var(--bg-glass-secondary)' }}>
              <img
                src="/images/gate-light.jpg"
                alt="ML Ingestion Gate"
                style={{ width: '100%', height: 'auto', borderRadius: '12px', mixBlendMode: 'multiply' }}
              />
            </div>
          </div>

          <div style={{ gridColumn: 'span 5', display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', color: 'var(--accent-indigo)', letterSpacing: '0.1em' }}>Integrity Guardrails</span>
            <h2 style={{ fontSize: '44px', fontWeight: 300, lineHeight: 1.1 }}>ML ingestion safety gates</h2>
            <p style={{ fontSize: '16px', lineHeight: 1.6, color: 'var(--text-secondary)' }}>
              Evaluate training datasets. Before pipeline runs trigger training, the ML gate checks composite compliance. If upstream trust decays below parameters, execution is blocked.
            </p>
          </div>

        </div>
      </section>

      {/* 7. AUTOMATED CODE GENERATION */}
      <section style={{ padding: '140px 64px', borderTop: '1px solid var(--border-color)' }}>
        <div style={{ width: '100%', maxWidth: '1500px', margin: '0 auto', display: 'grid', gridTemplateColumns: 'repeat(12, 1fr)', gap: '64px', alignItems: 'center' }}>
          
          <div style={{ gridColumn: 'span 6', display: 'flex', flexDirection: 'column', gap: '32px' }}>
            <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', color: 'var(--accent-indigo)', letterSpacing: '0.1em' }}>Synthesis Loop</span>
            <h2 style={{ fontSize: '44px', fontWeight: 300, lineHeight: 1.1 }}>Automated test synthesis</h2>
            <p style={{ fontSize: '16px', lineHeight: 1.6, color: 'var(--text-secondary)' }}>
              PRAXIS generates code-level test configurations to patch validation gaps. It compiles schema contracts and opens a GitHub PR to fix the broken parameters.
            </p>

            <div style={{ display: 'flex', gap: '20px', borderTop: '1px solid var(--border-color)', paddingTop: '24px' }}>
              <div style={{ opacity: pipelineState === 'detect' ? 1 : 0.4, transition: 'opacity 0.4s' }}>
                <span style={{ fontSize: '11px', fontWeight: 600, color: 'var(--accent-indigo)' }}>01 / DETECT</span>
                <span style={{ fontSize: '14px', fontWeight: 500, display: 'block', marginTop: '4px' }}>Schema drift alert</span>
              </div>
              <div style={{ opacity: pipelineState === 'generate' ? 1 : 0.4, transition: 'opacity 0.4s' }}>
                <span style={{ fontSize: '11px', fontWeight: 600, color: 'var(--accent-indigo)' }}>02 / COMPILE</span>
                <span style={{ fontSize: '14px', fontWeight: 500, display: 'block', marginTop: '4px' }}>dbt assertions</span>
              </div>
              <div style={{ opacity: pipelineState === 'pr' ? 1 : 0.4, transition: 'opacity 0.4s' }}>
                <span style={{ fontSize: '11px', fontWeight: 600, color: 'var(--accent-indigo)' }}>03 / PUSH</span>
                <span style={{ fontSize: '14px', fontWeight: 500, display: 'block', marginTop: '4px' }}>GitHub PR created</span>
              </div>
            </div>
          </div>

          <div style={{ gridColumn: 'span 6' }}>
            <div className="crystalline-surface" style={{ padding: '40px', fontFamily: 'var(--font-mono)', fontSize: '13px', background: '#FAF8F5' }}>
              {pipelineState === 'detect' && (
                <div style={{ color: 'var(--block)' }}>
                  <span style={{ fontWeight: 600 }}>[ALERT] SCHEMA_DRIFT:</span>
                  <p style={{ marginTop: '8px', color: 'var(--text-secondary)' }}>
                    "Field 'logging_events.user_id' type has changed from VARCHAR to INTEGER upstream. Dependent asset 'order_details' carries VARCHAR expectations."
                  </p>
                </div>
              )}
              {pipelineState === 'generate' && (
                <div style={{ color: 'var(--accent-indigo)' }}>
                  <span style={{ fontWeight: 600 }}>[COMPILED CONTRACT] schema.yaml:</span>
                  <pre style={{ marginTop: '12px', fontSize: '12px', color: 'var(--text-secondary)' }}>{`version: 2
models:
  - name: order_details
    columns:
      - name: user_id
        tests:
          - not_null
          - accepted_values:
              values: [1001, 1002, 1003]`}</pre>
                </div>
              )}
              {pipelineState === 'pr' && (
                <div style={{ color: 'var(--safe)' }}>
                  <span style={{ fontWeight: 600, display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <CheckCircle size={16} /> PR #104 DEPLOYED
                  </span>
                  <p style={{ marginTop: '8px', color: 'var(--text-secondary)' }}>
                    Branch `praxis/remediate-drift` has been pushed and a pull request opened against the master dbt schema repository.
                  </p>
                </div>
              )}
            </div>
          </div>

        </div>
      </section>

      {/* 8. DAILY INTEL MAGAZINE BRIEFING */}
      <section style={{ padding: '140px 64px', borderTop: '1px solid var(--border-color)', background: 'rgba(0,0,0,0.005)' }}>
        <div style={{ width: '100%', maxWidth: '1500px', margin: '0 auto', display: 'grid', gridTemplateColumns: 'repeat(12, 1fr)', gap: '64px', alignItems: 'center' }}>
          
          <div style={{ gridColumn: 'span 6' }}>
            <div className="crystalline-surface" style={{ padding: '48px', background: '#FAF8F5', display: 'flex', flexDirection: 'column', gap: '24px' }}>
              <div>
                <span style={{ fontSize: '11px', fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase' }}>Daily Briefing Summary</span>
                <h3 style={{ fontSize: '28px', marginTop: '8px', fontFamily: 'var(--font-serif)' }}>The executive briefing</h3>
              </div>
              <p style={{ fontSize: '14px', lineHeight: 1.6, color: 'var(--text-secondary)' }}>
                "Today, 4 out of 8 domains maintain full green compliance parameters. 12 datasets require review due to propagated upstream lineage warnings. 2 remediation branches have been opened on GitHub to address these gaps."
              </p>
            </div>
          </div>

          <div style={{ gridColumn: 'span 6', display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <span style={{ fontSize: '11px', fontWeight: 700, textTransform: 'uppercase', color: 'var(--accent-indigo)', letterSpacing: '0.1em' }}>Executive Summary</span>
            <h2 style={{ fontSize: '44px', fontWeight: 300, lineHeight: 1.1 }}>Editorial briefings</h2>
            <p style={{ fontSize: '16px', lineHeight: 1.6, color: 'var(--text-secondary)' }}>
              PRAXIS digests metadata changes into a human-readable summary, giving clear operational insight instead of raw logging lists.
            </p>
          </div>

        </div>
      </section>

      {/* 9. CTA TO WORKSPACE */}
      <section style={{ padding: '160px 80px', textAlign: 'center', borderTop: '1px solid var(--border-color)', background: 'var(--bg-glass-secondary)' }}>
        <div style={{ maxWidth: '800px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '32px', alignItems: 'center' }}>
          <span style={{ fontSize: '12px', fontWeight: 700, textTransform: 'uppercase', letterSpacing: '0.15em', color: 'var(--accent-indigo)' }}>Ready to monitor</span>
          <h2 style={{ fontSize: '64px', fontWeight: 300, lineHeight: 1.1 }}>Begin active orchestration</h2>
          <p style={{ fontSize: '18px', color: 'var(--text-secondary)', lineHeight: 1.6, maxWidth: '600px' }}>
            Enter the central operational room to inspect running agents, query the ML training safety gate, and view live metadata audits.
          </p>
          <div style={{ marginTop: '16px' }}>
            <Link href="/dashboard" className="btn-luxury btn-luxury-primary" style={{ padding: '18px 48px', fontSize: '16px' }}>
              Launch Dashboard
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer style={{
        padding: '100px 80px 60px 80px',
        background: '#121216',
        color: '#86868b',
        borderTop: '1px solid rgba(255,255,255,0.06)'
      }}>
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(12, 1fr)',
          gap: '64px',
          maxWidth: '1500px',
          margin: '0 auto'
        }}>
          <div style={{ gridColumn: 'span 4', display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <h4 style={{ color: '#fff', fontSize: '18px', fontWeight: 600, letterSpacing: '0.05em' }}>PRAXIS</h4>
            <p style={{ fontSize: '14px', lineHeight: 1.6 }}>
              Continuous Data Trust Intelligence platform for modern enterprise AI architectures.
            </p>
          </div>
          <div style={{ gridColumn: 'span 4' }}>
            <h5 style={{ color: '#fff', fontSize: '13px', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '20px' }}>Architecture</h5>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '14px' }}>
              <li><a href="#about" style={{ color: '#86868b', textDecoration: 'none' }}>Active Metadata</a></li>
              <li><a href="#scoring" style={{ color: '#86868b', textDecoration: 'none' }}>Deterministic Scoring</a></li>
              <li><a href="#gate" style={{ color: '#86868b', textDecoration: 'none' }}>ML Security Gate</a></li>
            </ul>
          </div>
          <div style={{ gridColumn: 'span 4' }}>
            <h5 style={{ color: '#fff', fontSize: '13px', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '20px' }}>Hackathon</h5>
            <ul style={{ listStyle: 'none', display: 'flex', flexDirection: 'column', gap: '12px', fontSize: '14px' }}>
              <li><a href="https://datahub.devpost.com" style={{ color: '#86868b', textDecoration: 'none' }}>Build with DataHub</a></li>
              <li><a href="https://github.com" style={{ color: '#86868b', textDecoration: 'none' }}>Repository</a></li>
            </ul>
          </div>
        </div>
        <div style={{
          maxWidth: '1500px',
          margin: '0 auto',
          marginTop: '80px',
          borderTop: '1px solid rgba(255,255,255,0.05)',
          paddingTop: '32px',
          display: 'flex',
          justifyContent: 'space-between',
          fontSize: '13px'
        }}>
          <span>&copy; 2026 PRAXIS. Built for the DataHub Agent Hackathon.</span>
        </div>
      </footer>

    </div>
  );
}
