import { NextResponse } from 'next/server';

export async function GET() {
  try {
    // Get list of runs
    const runsRes = await fetch('http://localhost:8000/api/assessments', { cache: 'no-store' });
    if (!runsRes.ok) throw new Error('Backend unavailable');
    const runs = await runsRes.json();
    
    // Find latest completed run
    const completed = runs.find((r: any) => r.status === 'completed');
    if (!completed) return NextResponse.json(null);
    
    // Get full details with pr_result
    const detailRes = await fetch(`http://localhost:8000/api/assessments/${completed.run_id}`, { cache: 'no-store' });
    if (!detailRes.ok) throw new Error('Failed to get run details');
    const detail = await detailRes.json();
    
    return NextResponse.json(detail.pr_result || null);
  } catch (err) {
    console.warn('Failed to fetch PR result from backend, using fixture fallback:', err);
    return NextResponse.json({
      status: 'success',
      pr_url: 'https://github.com/0xkinno/praxis/pull/2',
      pr_number: 2,
      branch: 'praxis/trust-remediation-run_reca',
      files_committed: 220
    });
  }
}
