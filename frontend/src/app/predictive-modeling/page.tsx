"use client"; 

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft, TrendingUp, BarChart3, Target, Activity } from "lucide-react";
import { BackButton } from "@/src/components/ui/BackButton";

export default function PredictiveModeling() {

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="border-b">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center gap-4">
            <BackButton />
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-gradient-success">
                <TrendingUp className="h-5 w-5 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">Predictive Modeling Engine</h1>
                <p className="text-sm text-muted-foreground">ML-powered forecasting models</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Growth Trends */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5 text-primary" />
                Historical Growth
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary mb-1">$391.04B</div>
                  <p className="text-sm text-muted-foreground">FY 2024 Revenue</p>
                </div>
                
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm">Revenue Growth</span>
                    <span className="font-semibold text-green-500">+2.8% YoY</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm">Net Income</span>
                    <span className="font-semibold">$93.74B</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm">EPS</span>
                    <span className="font-semibold">$6.08</span>
                  </div>
                </div>
                
                <div className="p-3 rounded-lg bg-muted/50">
                  <p className="text-xs">
                    <strong>Trend:</strong> Steady revenue growth with strong profitability metrics despite market headwinds.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Simple Forecasting */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Target className="h-5 w-5 text-accent" />
                Basic Projections
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="p-3 rounded-lg bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800">
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-medium text-green-700 dark:text-green-300">Optimistic</span>
                    <span className="text-green-600 font-semibold">$420B</span>
                  </div>
                  <p className="text-xs text-green-600 dark:text-green-400">+7.5% growth (FY 2025)</p>
                </div>
                <div className="p-3 rounded-lg bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800">
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-medium text-blue-700 dark:text-blue-300">Expected</span>
                    <span className="text-blue-600 font-semibold">$405B</span>
                  </div>
                  <p className="text-xs text-blue-600 dark:text-blue-400">+3.5% growth (FY 2025)</p>
                </div>
                <div className="p-3 rounded-lg bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800">
                  <div className="flex justify-between items-center mb-1">
                    <span className="font-medium text-orange-700 dark:text-orange-300">Conservative</span>
                    <span className="text-orange-600 font-semibold">$395B</span>
                  </div>
                  <p className="text-xs text-orange-600 dark:text-orange-400">+1% growth (FY 2025)</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Key Metrics */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="h-5 w-5 text-warning" />
                Key Assumptions
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="space-y-2">
                  <h4 className="font-medium text-sm">Based on Historical Data:</h4>
                  <div className="flex justify-between text-sm">
                    <span>Avg Revenue Growth</span>
                    <span className="font-medium">5.2%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Gross Margin</span>
                    <span className="font-medium">46.2%</span>
                  </div>
                  <div className="flex justify-between text-sm">
                    <span>Operating Margin</span>
                    <span className="font-medium">31.5%</span>
                  </div>
                </div>
                
                <div className="pt-3 border-t">
                  <h4 className="font-medium text-sm mb-2">Market Factors:</h4>
                  <ul className="text-xs space-y-1">
                    <li>• Services growth momentum</li>
                    <li>• iPhone replacement cycles</li>
                    <li>• Geographic expansion</li>
                    <li>• New product categories</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Methodology */}
          <Card className="shadow-card lg:col-span-3">
            <CardHeader>
              <CardTitle>Simple Forecasting Methodology</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold mb-3">Data Sources Available</h4>
                  <div className="space-y-2 text-sm">
                    <p><strong>Income Statement:</strong> Revenue, costs, margins from FMP API</p>
                    <p><strong>Financial Ratios:</strong> Profitability, efficiency, and leverage metrics</p>
                    <p><strong>Growth Metrics:</strong> Historical performance indicators</p>
                    <p><strong>Market Data:</strong> Stock price, valuation multiples</p>
                  </div>
                  
                  <h4 className="font-semibold mb-3 mt-6">Simple Models Used</h4>
                  <ul className="space-y-1 text-sm">
                    <li>• Trend analysis (3-year average growth)</li>
                    <li>• Margin stability assumptions</li>
                    <li>• Segment growth differentials</li>
                    <li>• Market multiple comparisons</li>
                  </ul>
                </div>
                
                <div>
                  <h4 className="font-semibold mb-3">Limitations & Considerations</h4>
                  <div className="space-y-2 text-sm">
                    <p><strong>Model Simplicity:</strong> Basic trend extrapolation, not sophisticated ML</p>
                    <p><strong>Data Scope:</strong> Limited to available FMP endpoints</p>
                    <p><strong>External Factors:</strong> Macro conditions not fully captured</p>
                  </div>
                  
                  <div className="mt-4 p-3 rounded-lg bg-muted/50">
                    <p className="text-xs">
                      <strong>Recommendation:</strong> Use these projections as directional guidance. Actual results will depend on product cycles, market conditions, and competitive dynamics not captured in historical financials.
                    </p>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}