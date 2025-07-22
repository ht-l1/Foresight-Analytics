"use client"; 

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowLeft, Newspaper, TrendingUp, AlertTriangle, Clock } from "lucide-react";
import { BackButton } from "@/src/components/ui/BackButton";

export default function MarketIntelligence() {

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <div className="border-b">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center gap-4">
            <BackButton />
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-secondary">
                <Newspaper className="h-5 w-5 text-white" />
              </div>
              <div>
                <h1 className="text-2xl font-bold">Market Intelligence</h1>
                <p className="text-sm text-muted-foreground">Latest financial news & updates</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-6xl mx-auto px-6 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Market Sentiment */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-primary" />
                Market Sentiment
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-500 mb-1">72%</div>
                  <p className="text-sm text-muted-foreground">Positive Sentiment</p>
                  <p className="text-xs text-green-500">+5% from last week</p>
                </div>
                
                <div className="space-y-2">
                  <div className="flex justify-between">
                    <span className="text-sm">Bullish Articles</span>
                    <span className="font-semibold text-green-500">124</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm">Neutral Articles</span>
                    <span className="font-semibold text-accent">87</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-sm">Bearish Articles</span>
                    <span className="font-semibold text-red-500">43</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Risk Assessment */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="h-5 w-5 text-warning" />
                Risk Assessment
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="p-3 rounded-lg bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800">
                  <div className="flex items-center gap-2 mb-1">
                    <Badge variant="destructive" className="text-xs">High</Badge>
                    <span className="font-medium text-sm">Regulatory Risk</span>
                  </div>
                  <p className="text-xs text-red-600 dark:text-red-400">AI regulation discussions in EU parliament</p>
                </div>
                
                <div className="p-3 rounded-lg bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800">
                  <div className="flex items-center gap-2 mb-1">
                    <Badge variant="secondary" className="text-xs bg-orange-100 text-orange-800">Medium</Badge>
                    <span className="font-medium text-sm">Competition</span>
                  </div>
                  <p className="text-xs text-orange-600 dark:text-orange-400">New entrants in financial AI space</p>
                </div>
                
                <div className="p-3 rounded-lg bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800">
                  <div className="flex items-center gap-2 mb-1">
                    <Badge variant="outline" className="text-xs border-green-500 text-green-700">Low</Badge>
                    <span className="font-medium text-sm">Market Risk</span>
                  </div>
                  <p className="text-xs text-green-600 dark:text-green-400">Stable demand for analytics tools</p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Data Sources */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Clock className="h-5 w-5 text-accent" />
                Live Data Feed
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-sm">FMP Articles</span>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-green-500"></div>
                    <span className="text-xs">Live</span>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm">Market Data</span>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-green-500"></div>
                    <span className="text-xs">Real-time</span>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-sm">Social Sentiment</span>
                  <div className="flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-green-500"></div>
                    <span className="text-xs">15min delay</span>
                  </div>
                </div>
                
                <div className="pt-2 border-t">
                  <p className="text-xs text-muted-foreground">
                    Last update: 2 minutes ago
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Recent News */}
          <Card className="shadow-card lg:col-span-2">
            <CardHeader>
              <CardTitle>Latest Financial News</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="p-4 rounded-lg border border-primary/20 bg-primary/5">
                  <div className="flex items-start justify-between mb-2">
                    <h4 className="font-semibold text-primary">Tech Giants Report Strong Q4 Earnings</h4>
                    <Badge variant="outline" className="text-xs">Breaking</Badge>
                  </div>
                  <p className="text-sm text-muted-foreground mb-2">
                    Major technology companies exceed analyst expectations with cloud revenue driving growth across the sector.
                  </p>
                  <div className="flex items-center gap-4 text-xs text-muted-foreground">
                    <span>2 hours ago</span>
                    <span>Impact: High</span>
                    <span className="text-green-500">Sentiment: Positive</span>
                  </div>
                </div>

                <div className="p-4 rounded-lg border">
                  <h4 className="font-semibold mb-2">Federal Reserve Maintains Current Interest Rates</h4>
                  <p className="text-sm text-muted-foreground mb-2">
                    Fed officials signal cautious approach to monetary policy amid economic uncertainty and inflation concerns.
                  </p>
                  <div className="flex items-center gap-4 text-xs text-muted-foreground">
                    <span>4 hours ago</span>
                    <span>Impact: Medium</span>
                    <span className="text-blue-500">Sentiment: Neutral</span>
                  </div>
                </div>

                <div className="p-4 rounded-lg border">
                  <h4 className="font-semibold mb-2">AI Regulation Framework Proposed in Europe</h4>
                  <p className="text-sm text-muted-foreground mb-2">
                    European Parliament discusses comprehensive AI governance framework affecting financial services automation.
                  </p>
                  <div className="flex items-center gap-4 text-xs text-muted-foreground">
                    <span>6 hours ago</span>
                    <span>Impact: High</span>
                    <span className="text-orange-500">Sentiment: Cautious</span>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Impact Analysis */}
          <Card className="shadow-card">
            <CardHeader>
              <CardTitle>Impact Analysis</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <h4 className="font-medium mb-2">Revenue Impact</h4>
                  <div className="space-y-2">
                    <div className="flex justify-between">
                      <span className="text-sm">Positive Drivers</span>
                      <span className="font-semibold text-green-500">+$85M</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-sm">Risk Factors</span>
                      <span className="font-semibold text-red-500">-$23M</span>
                    </div>
                    <div className="flex justify-between border-t pt-2">
                      <span className="font-medium">Net Impact</span>
                      <span className="font-bold text-green-500">+$62M</span>
                    </div>
                  </div>
                </div>
                
                <div>
                  <h4 className="font-medium mb-2">Key Recommendations</h4>
                  <ul className="space-y-1 text-sm">
                    <li>• Accelerate enterprise sales in Q1</li>
                    <li>• Monitor EU regulation developments</li>
                    <li>• Increase R&D investment in AI compliance</li>
                    <li>• Diversify revenue streams geographically</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}