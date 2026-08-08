
import { NextResponse } from 'next/server';
import { MOCK_CATALOG } from '@/lib/fixtures';

export async function GET() {
  return NextResponse.json(MOCK_CATALOG);
}
