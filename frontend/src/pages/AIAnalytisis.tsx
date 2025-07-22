import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft, Brain, TrendingUp, AlertCircle, CheckCircle } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function AIAnalysis() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="border-b">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center gap-4">
            <Button
              variant="outline"
              size="sm"
              onClick={() => navigate('/')}
              className="flex items-center gap-2"
            >
              <ArrowLeft className="h-4 w-4" />
              Back to Dashboard
            </Button>
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-gradient-primary">
                <Brain className="h-5 w-5 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">AI Financial Analysis</h1>
                <p className="text-sm text-muted-foreground">Automated insights & commentary</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Key Ratios Analysis */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-primary" />
                Financial Ratios Analysis
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="space-y-3">
                  <div className="flex justify-between">
                    <span className="text-sm">Gross Profit Margin</span>
                    <span className="font-semibold text-green-500">46.21%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm">Operating Margin</span>
                    <span className="font-semibold text-primary">31.51%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm">Net Profit Margin</span>
                    <span className="font-semibold text-accent">23.97%</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm">Return on Equity</span>
                    <span className="font-semibold text-green-500">164.59%</span>
                  </div>
                </div>
                <div className="p-4 rounded-lg border border-primary/20 bg-primary/5">
                  <p className="text-sm">
                    <strong>AI Insight:</strong> Exceptional profitability metrics with ROE significantly above industry average. Strong operational efficiency with improving margin trends.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Valuation Metrics */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Brain className="h-5 w-5 text-accent" />
                Valuation Analysis
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-sm">P/E Ratio</span>
                  <span className="font-semibold">37.29x</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">P/S Ratio</span>
                  <span className="font-semibold">8.94x</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">P/B Ratio</span>
                  <span className="font-semibold">61.37x</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-sm">EV/EBITDA</span>
                  <span className="font-semibold">26.62x</span>
                </div>
                
                <div className="pt-3 border-t space-y-2">
                  <div className="flex items-start gap-3">
                    <AlertCircle className="h-4 w-4 text-warning mt-0.5" />
                    <div>
                      <p className="text-sm font-medium">Premium Valuation</p>
                      <p className="text-xs text-muted-foreground">Trading at premium to sector average</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3">
                    <CheckCircle className="h-4 w-4 text-green-500 mt-0.5" />
                    <div>
                      <p className="text-sm font-medium">Strong Fundamentals</p>
                      <p className="text-xs text-muted-foreground">Justified by superior growth and margins</p>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Financial Health */}
          <Card className="shadow-card lg:col-span-2">
            <CardHeader>
              <CardTitle>Financial Health Assessment</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold mb-3">Liquidity Analysis</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span>Current Ratio</span>
                      <span className="font-medium">0.87x</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Quick Ratio</span>
                      <span className="font-medium">0.83x</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Cash Ratio</span>
                      <span className="font-medium">0.17x</span>
                    </div>
                  </div>
                  
                  <h4 className="font-semibold mb-3 mt-4">Leverage Analysis</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span>Debt-to-Assets</span>
                      <span className="font-medium">32.62%</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Debt-to-Equity</span>
                      <span className="font-medium">2.09x</span>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h4 className="font-semibold mb-3">Efficiency Metrics</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span>Asset Turnover</span>
                      <span className="font-medium">1.07x</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Inventory Turnover</span>
                      <span className="font-medium">28.87x</span>
                    </div>
                    <div className="flex justify-between">
                      <span>Free Cash Flow Yield</span>
                      <span className="font-medium text-green-500">3.11%</span>
                    </div>
                  </div>
                  
                  <div className="mt-4 p-3 rounded-lg bg-muted/50">
                    <p className="text-xs">
                      <strong>AI Summary:</strong> Strong profitability with premium valuation justified by exceptional margins and growth. Monitor liquidity ratios but overall financial health is robust.
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