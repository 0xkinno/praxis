
import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  const body = await request.json();
  const source_urns = body || [];
  
  const has_logging = source_urns.some((urn: string) => urn.includes('logging_events'));
  const has_details = source_urns.some((urn: string) => urn.includes('order_details'));
  
  if (has_logging) {
    return NextResponse.json({
      verdict: "BLOCK_TRAINING",
      summary: "ML Training Blocked: Upstream source 'logging_events' has critical quality risk (<40).",
      recommendation: "Do NOT train. Resolve underlying schema stability gaps on 'logging_events' before retrying.",
      sources: source_urns.map((urn: string) => ({
        urn,
        name: urn.split(':').pop() || urn,
        score: urn.includes('order_details') ? 72.0 : 90.0,
        grade: urn.includes('order_details') ? "C+" : "A",
        status: "OK"
      })),
      upstream_risks: [
        {
          urn: "urn:li:dataset:(urn:li:dataPlatform:hive,logging_events,PROD)",
          name: "logging_events",
          score: 33.8,
          grade: "F",
          hop: 1,
          reason: "Severe lack of ownership and description metadata."
        }
      ]
    });
  } else if (has_details) {
    return NextResponse.json({
      verdict: "CAUTION",
      summary: "ML Training Caution: Direct source 'order_details' requires quality SLA review.",
      recommendation: "Proceed with caution. Monitor validation loops closely during the run.",
      sources: source_urns.map((urn: string) => ({
        urn,
        name: "order_details",
        score: 72.0,
        grade: "C+",
        status: "OK"
      })),
      upstream_risks: []
    });
  } else {
    return NextResponse.json({
      verdict: "SAFE_TO_TRAIN",
      summary: "All sources and upstream lineage are certified as trusted.",
      recommendation: "Safe to train. Pipeline execution can proceed.",
      sources: source_urns.map((urn: string) => ({
        urn,
        name: urn.split(':').pop() || urn,
        score: 90.0,
        grade: "A",
        status: "OK"
      })),
      upstream_risks: []
    });
  }
}
