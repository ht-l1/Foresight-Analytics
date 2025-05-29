export interface ForecastData {
  date: string;
  value: number;
  confidence_lower?: number;
  confidence_upper?: number;
}

export interface ModelMetrics {
  accuracy: number;
  mape: number;
  r2_score: number;
  cross_val_score: number;
}

export interface ForecastResult {
  forecasts: {
    [modelName: string]: ForecastData[];
  };
  metrics: {
    [modelName: string]: ModelMetrics;
  };
}

export interface FilterOptions {
  region?: string;
  category?: string;
  months?: number;
}

export interface DataPoint {
  order_date: string;
  region: string;
  category: string;
  segment: string;
  sales: number;
  quantity: number;
  discount: number;
  profit: number;
}

export interface ApiResponse<T> {
  status: string;
  data: T;
  metadata?: any;
}