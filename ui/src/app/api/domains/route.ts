
import { NextResponse } from 'next/server';
import { MOCK_DOMAINS } from '@/lib/fixtures';

export async function GET() {
  return NextResponse.json(MOCK_DOMAINS);
}
