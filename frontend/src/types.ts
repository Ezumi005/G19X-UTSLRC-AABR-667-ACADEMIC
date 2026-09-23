export interface CustomerRow {
  customer_id: string;
  age: number | null;
  city: string | null;
  registered_at: string;
  cluster_id: number | null;
  segment_label: string | null;
}

export interface CustomersPage {
  total: number;
  count: number;
  data: CustomerRow[];
}

export interface CustomerDetail {
  customer_id: string;
  age: number | null;
  city: string | null;
  registered_at: string;
  stats: {
    frequency: number;
    monetary: number;
    last_purchase: string | null;
    categories_count: number;
  };
  segment: { segment_id: number; label: string; cluster_id: number } | null;
}

export interface Segment {
  segment_id: number;
  cluster_id: number;
  label: string;
  description: string | null;
  n_customers: number;
  profile: Record<string, number | null>;
}

export interface SegmentsPage {
  run_id: number | null;
  count: number;
  data: Segment[];
}

export interface SegmentDetail extends Segment {
  run_id: number;
  k: number;
  metrics: Record<string, number>;
  started_at: string;
  run_status: string;
  customers_preview: { customer_id: string; city: string | null; registered_at: string }[];
}

export interface Dashboard {
  total_customers: number;
  total_transactions: number;
  total_spend: number;
  avg_ticket: number;
  last_ingestion: { run_id: number; status: string; finished_at: string } | null;
  last_segmentation: { run_id: number; k: number; n_customers: number; started_at: string } | null;
  segments_distribution: { segment_id: number; label: string; n_customers: number }[];
}
