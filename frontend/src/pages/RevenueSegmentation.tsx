import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ArrowLeft, PieChart, BarChart3, Globe, Users } from "lucide-react";
import { useNavigate } from "react-router-dom";

export default function RevenueSegmentation() {
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
              <div className="p-2 rounded-lg bg-primary">
                <PieChart className="h-5 w-5 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">Revenue Segmentation</h1>
                <p className="text-sm text-muted-foreground">Product & segment analysis</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Product Revenue Breakdown */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <PieChart className="h-5 w-5 text-primary" />
                Product Revenue Mix (FY 2024)
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">iPhone</span>
                    <span className="font-semibold">$201.18B (51.4%)</span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-3">
                    <div className="bg-primary h-3 rounded-full w-[51.4%]"></div>
                  </div>
                </div>
                
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Services</span>
                    <span className="font-semibold">$96.17B (24.6%)</span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-3">
                    <div className="bg-accent h-3 rounded-full w-[24.6%]"></div>
                  </div>
                </div>
                
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Wearables & Accessories</span>
                    <span className="font-semibold">$37.01B (9.5%)</span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-3">
                    <div className="bg-warning h-3 rounded-full w-[9.5%]"></div>
                  </div>
                </div>
                
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">Mac</span>
                    <span className="font-semibold">$29.98B (7.7%)</span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-3">
                    <div className="bg-secondary h-3 rounded-full w-[7.7%]"></div>
                  </div>
                </div>
                
                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm">iPad</span>
                    <span className="font-semibold">$26.69B (6.8%)</span>
                  </div>
                  <div className="w-full bg-muted rounded-full h-3">
                    <div className="bg-muted-foreground h-3 rounded-full w-[6.8%]"></div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Geographic Revenue Distribution */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Globe className="h-5 w-5 text-accent" />
                Geographic Revenue (FY 2024)
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="p-4 rounded-lg bg-blue-50 dark:bg-blue-900/20">
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-medium">Americas</span>
                    <span className="font-bold text-blue-600">$167.05B (42.7%)</span>
                  </div>
                  <p className="text-xs text-blue-600">Largest revenue contributor</p>
                </div>
                
                <div className="p-4 rounded-lg bg-green-50 dark:bg-green-900/20">
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-medium">Europe</span>
                    <span className="font-bold text-green-600">$101.33B (25.9%)</span>
                  </div>
                  <p className="text-xs text-green-600">Strong European presence</p>
                </div>
                
                <div className="p-4 rounded-lg bg-orange-50 dark:bg-orange-900/20">
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-medium">Greater China</span>
                    <span className="font-bold text-orange-600">$66.95B (17.1%)</span>
                  </div>
                  <p className="text-xs text-orange-600">Key growth market</p>
                </div>
                
                <div className="p-4 rounded-lg bg-purple-50 dark:bg-purple-900/20">
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-medium">Rest of Asia Pacific</span>
                    <span className="font-bold text-purple-600">$30.66B (7.8%)</span>
                  </div>
                  <p className="text-xs text-purple-600">Emerging markets</p>
                </div>
                
                <div className="p-4 rounded-lg bg-pink-50 dark:bg-pink-900/20">
                  <div className="flex justify-between items-center mb-2">
                    <span className="font-medium">Japan</span>
                    <span className="font-bold text-pink-600">$25.05B (6.4%)</span>
                  </div>
                  <p className="text-xs text-pink-600">Mature market</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Segment Analysis */}
          <Card className="shadow-card lg:col-span-2">
            <CardHeader>
              <CardTitle>Revenue Segment Insights</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 className="font-semibold mb-3">Product Performance</h4>
                  <div className="space-y-3">
                    <div className="p-3 rounded-lg bg-muted/50">
                      <div className="flex justify-between items-center mb-1">
                        <span className="font-medium">iPhone Dominance</span>
                        <span className="text-sm text-primary">51.4%</span>
                      </div>
                      <p className="text-xs text-muted-foreground">Core product driving majority of revenue</p>
                    </div>
                    <div className="p-3 rounded-lg bg-muted/50">
                      <div className="flex justify-between items-center mb-1">
                        <span className="font-medium">Services Growth</span>
                        <span className="text-sm text-accent">24.6%</span>
                      </div>
                      <p className="text-xs text-muted-foreground">High-margin recurring revenue stream</p>
                    </div>
                    <div className="p-3 rounded-lg bg-muted/50">
                      <div className="flex justify-between items-center mb-1">
                        <span className="font-medium">Ecosystem Products</span>
                        <span className="text-sm text-warning">23.0%</span>
                      </div>
                      <p className="text-xs text-muted-foreground">Mac, iPad, Wearables supporting ecosystem</p>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h4 className="font-semibold mb-3">Geographic Distribution</h4>
                  <div className="space-y-2 text-sm">
                    <div className="flex justify-between">
                      <span>Americas Revenue</span>
                      <span className="font-semibold">42.7%</span>
                    </div>
                    <div className="flex justify-between">
                      <span>International Revenue</span>
                      <span className="font-semibold">57.3%</span>
                    </div>
                    <div className="flex justify-between">
                      <span>China Exposure</span>
                      <span className="font-semibold">17.1%</span>
                    </div>
                  </div>
                  
                  <div className="mt-4 p-3 rounded-lg bg-muted/50">
                    <p className="text-xs">
                      <strong>Key Insight:</strong> Well-diversified geographic revenue with strong international presence. iPhone remains core driver while Services provides high-margin growth.
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