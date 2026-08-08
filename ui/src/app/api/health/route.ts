
import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    status: "healthy",
    mode: "fixture",
    datahub: "fixture_bypass",
    database: "ready"
  });
}
