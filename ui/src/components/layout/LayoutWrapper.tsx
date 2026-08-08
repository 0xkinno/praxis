'use client';

import { usePathname } from 'next/navigation';
import { motion, AnimatePresence } from 'framer-motion';
import { useEffect, useRef } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';

export default function LayoutWrapper({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const isLanding = pathname === '/';
  const canvasRef = useRef<HTMLCanvasElement>(null);

  // Dynamic canvas-based architectural background rendering slow-moving contour waves
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    let width = (canvas.width = window.innerWidth);
    let height = (canvas.height = window.innerHeight);
    let mouseX = width / 2;
    let mouseY = height / 2;

    const handleResize = () => {
      width = canvas.width = window.innerWidth;
      height = canvas.height = window.innerHeight;
    };

    const handleMouseMove = (e: MouseEvent) => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    };

    window.addEventListener('resize', handleResize);
    window.addEventListener('mousemove', handleMouseMove);

    // Wave parameters representing flowing data topologies / structural contours
    const waves = [
      { amplitude: 60, frequency: 0.002, speed: 0.003, color: 'rgba(29, 29, 31, 0.015)', verticalOffset: 0.2 },
      { amplitude: 90, frequency: 0.0015, speed: 0.002, color: 'rgba(44, 27, 140, 0.01)', verticalOffset: 0.35 },
      { amplitude: 40, frequency: 0.003, speed: 0.004, color: 'rgba(13, 99, 214, 0.008)', verticalOffset: 0.5 },
      { amplitude: 80, frequency: 0.001, speed: 0.0015, color: 'rgba(29, 29, 31, 0.01)', verticalOffset: 0.65 }
    ];

    let t = 0;

    const render = () => {
      t += 0.8;
      ctx.clearRect(0, 0, width, height);

      // Base environment color: rich slate stone gradient
      const bgGrad = ctx.createLinearGradient(0, 0, width, height);
      bgGrad.addColorStop(0, '#121216');
      bgGrad.addColorStop(0.5, '#191921');
      bgGrad.addColorStop(1, '#0e0e12');
      ctx.fillStyle = bgGrad;
      ctx.fillRect(0, 0, width, height);

      // Draw subtle architectural vertical grid lines
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.008)';
      ctx.lineWidth = 1;
      const gridSize = 120;
      for (let x = 0; x < width; x += gridSize) {
        ctx.beginPath();
        ctx.moveTo(x, 0);
        ctx.lineTo(x, height);
        ctx.stroke();
      }

      // Draw slow-moving dynamic wave contours representing lineage flows
      waves.forEach((wave, idx) => {
        ctx.beginPath();
        ctx.strokeStyle = wave.color;
        ctx.lineWidth = idx === 1 ? 2.5 : 1.5;

        for (let x = 0; x < width; x += 4) {
          // Compute wave elevation using sine math + displacement from cursor
          const xOffset = x * wave.frequency + t * wave.speed;
          const cursorDist = Math.abs(x - mouseX);
          const cursorFactor = cursorDist < 400 ? (1 - cursorDist / 400) * 35 : 0;
          
          const y = 
            height * wave.verticalOffset + 
            Math.sin(xOffset) * wave.amplitude + 
            Math.cos(xOffset * 0.5) * (wave.amplitude * 0.3) +
            Math.sin((mouseY - height / 2) * 0.002) * cursorFactor;

          if (x === 0) {
            ctx.moveTo(x, y);
          } else {
            ctx.lineTo(x, y);
          }
        }
        ctx.stroke();
      });

      // Draw localized cursor proximity illumination (subtle volumetric light field behind the viewport frame)
      const spotlight = ctx.createRadialGradient(mouseX, mouseY, 50, mouseX, mouseY, 600);
      spotlight.addColorStop(0, 'rgba(44, 27, 140, 0.03)');
      spotlight.addColorStop(0.5, 'rgba(95, 37, 159, 0.015)');
      spotlight.addColorStop(1, 'rgba(0, 0, 0, 0)');
      ctx.fillStyle = spotlight;
      ctx.fillRect(0, 0, width, height);

      animationFrameId = requestAnimationFrame(render);
    };

    render();

    return () => {
      window.removeEventListener('resize', handleResize);
      window.removeEventListener('mousemove', handleMouseMove);
      cancelAnimationFrame(animationFrameId);
    };
  }, []);

  return (
    <>
      {/* Dynamic environmental lines field */}
      <canvas
        ref={canvasRef}
        style={{
          position: 'fixed',
          top: 0,
          left: 0,
          width: '100vw',
          height: '100vh',
          zIndex: 0,
          pointerEvents: 'none'
        }}
      />

      {/* Centered Crystalline Frame Canvas */}
      <div className="viewport-frame-canvas">
        <AnimatePresence mode="wait">
          {isLanding ? (
            <motion.div
              key="landing"
              initial={{ opacity: 0, scale: 0.97, filter: 'blur(10px)' }}
              animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
              exit={{ opacity: 0, scale: 1.03, filter: 'blur(10px)' }}
              transition={{ duration: 0.45, ease: [0.16, 1, 0.3, 1] }}
              style={{ flex: 1, display: 'flex', flexDirection: 'column', height: '100%', overflowY: 'auto' }}
            >
              {children}
            </motion.div>
          ) : (
            <motion.div
              key="dashboard-workspace"
              initial={{ opacity: 0, scale: 1.03, filter: 'blur(10px)' }}
              animate={{ opacity: 1, scale: 1, filter: 'blur(0px)' }}
              exit={{ opacity: 0, scale: 0.97, filter: 'blur(10px)' }}
              transition={{ duration: 0.45, ease: [0.16, 1, 0.3, 1] }}
              style={{ display: 'flex', flex: 1, minWidth: 0, height: '100%', overflow: 'hidden' }}
            >
              <Sidebar />
              <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0, height: '100%' }}>
                <Header />
                <main style={{ flex: 1, padding: '40px', overflowY: 'auto', position: 'relative' }}>
                  {children}
                </main>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </>
  );
}
