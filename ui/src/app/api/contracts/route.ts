
import { NextResponse } from 'next/server';
import { MOCK_CONTRACTS } from '@/lib/fixtures';

export async function GET() {
  return NextResponse.json(MOCK_CONTRACTS);
}
