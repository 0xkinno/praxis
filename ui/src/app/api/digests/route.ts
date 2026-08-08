
import { NextResponse } from 'next/server';
import { MOCK_RUNS } from '@/lib/fixtures';

export async function GET() {
  return NextResponse.json(MOCK_RUNS.map(r => ({
    run_id: r.run_id,
    date: r.completed_at ? new Date(r.completed_at).toISOString().split('T')[0] : "Unknown",
    title: `PRAXIS Daily Trust Digest - ${r.completed_at ? new Date(r.completed_at).toISOString().split('T')[0] : "Digest"}`
  })));
}
