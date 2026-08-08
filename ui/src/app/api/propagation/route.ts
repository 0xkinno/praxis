
import { NextResponse } from 'next/server';
import { MOCK_PROPAGATION } from '@/lib/fixtures';

export async function GET() {
  return NextResponse.json(MOCK_PROPAGATION);
}
