
import { NextResponse } from 'next/server';
import { MOCK_RUNS } from '@/lib/fixtures';

export async function GET() {
  return NextResponse.json(MOCK_RUNS);
}

export async function POST() {
  return NextResponse.json({
    run_id: "run_demo_1234",
    status: "running",
    mode: "fixture"
  });
}
