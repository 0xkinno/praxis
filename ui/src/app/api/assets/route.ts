
import { NextResponse } from 'next/server';
import { MOCK_ASSETS } from '@/lib/fixtures';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const domain = searchParams.get('domain');
  const platform = searchParams.get('platform');
  const tier = searchParams.get('tier');
  
  let assets = [...MOCK_ASSETS];
  if (domain) assets = assets.filter(a => a.domain.toLowerCase() === domain.toLowerCase());
  if (platform) assets = assets.filter(a => a.platform.toLowerCase() === platform.toLowerCase());
  if (tier) assets = assets.filter(a => a.tier.toLowerCase() === tier.toLowerCase());
  
  return NextResponse.json(assets);
}
