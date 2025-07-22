"use client";

import { Button } from "@/src/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/src/components/ui/card";
import { Badge } from "@/src/components/ui/badge";
import { 
  TrendingUp, 
  Brain, 
  BarChart3, 
  Newspaper, 
  Target, 
  PieChart,
  Activity,
  DollarSign,
  Users,
  Calendar
} from "lucide-react";
import { useRouter } from "next/navigation";

export function FinancePlatform() {
    const router = useRouter(); 

  const handleCardClick = (path: string) => {
    router.push(path);
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Hero Section */}
      <section className="relative bg-gradient-hero text-white py-12 px-6 overflow-hidden">
        <div className="absolute inset-0 bg-black/40"></div>
        <div className="relative max-w-6xl mx-auto text-center">
          <div className="animate-fade-in">
            <Badge className="mb-4 bg-white/20 text-white border-white/30">
              Enterprise AI Financial Analytics
            </Badge>
            <h1 className="text-3xl md:text-4xl font-bold mb-4 leading-tight">
              AI-Powered Financial
              <span className="text-primary-glow"> Intelligence Platform</span>
            </h1>
            <p className="text-lg mb-6 text-white/90 max-w-2xl mx-auto">
              Advanced ML forecasting, automated FP&A reports, and intelligent market analysis.
            </p>
            <div className="flex flex-col sm:flex-row gap-3 justify-center">
              <Button variant="financial" className="px-6">
                <Activity className="mr-2 h-4 w-4" />
                Start Analysis
              </Button>
              <Button variant="outline" className="px-6 border-white text-white hover:bg-white hover:text-primary">
                <BarChart3 className="mr-2 h-4 w-4" />
                View Demo
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Key Metrics Overview */}
      <section className="py-8 px-6 bg-muted/50">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-4 animate-slide-up">
            <Card className="shadow-card hover:shadow-elegant transition-all duration-300">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">
                  Active Models
                </CardTitle>
                <Brain className="h-4 w-4 text-primary" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-primary">3</div>
                <p className="text-xs text-muted-foreground">
                  ML Forecasting Models
                </p>
              </CardContent>
            </Card>

            <Card className="shadow-card hover:shadow-elegant transition-all duration-300">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">
                  Data Sources
                </CardTitle>
                <Activity className="h-4 w-4 text-accent" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-accent">Live</div>
                <p className="text-xs text-muted-foreground">
                  FMP API Integration
                </p>
              </CardContent>
            </Card>

            <Card className="shadow-card hover:shadow-elegant transition-all duration-300">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">
                  Companies Tracked
                </CardTitle>
                <Users className="h-4 w-4 text-warning" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-warning">FAANG</div>
                <p className="text-xs text-muted-foreground">
                  Tech Giants Focus
                </p>
              </CardContent>
            </Card>

            <Card className="shadow-card hover:shadow-elegant transition-all duration-300">
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium text-muted-foreground">
                  Forecast Horizon
                </CardTitle>
                <Calendar className="h-4 w-4 text-destructive" />
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold text-destructive">5Y</div>
                <p className="text-xs text-muted-foreground">
                  Historical + Predictions
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Main Features */}
      <section className="py-8 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-8">
            <h2 className="text-2xl font-bold mb-3">Comprehensive Financial Analytics</h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Enterprise-grade financial intelligence with ML forecasting and automated reporting.
            </p>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* AI Financial Analysis */}
            <Card 
              className="shadow-card hover:shadow-elegant transition-all duration-300 cursor-pointer hover:scale-105"
              onClick={() => handleCardClick('/ai-analysis')}
            >
              <CardHeader className="pb-3">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-gradient-primary">
                    <Brain className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <CardTitle className="text-lg">AI Financial Analysis</CardTitle>
                    <p className="text-sm text-muted-foreground">Automated insights & commentary</p>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="pt-0 space-y-3">
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-accent"></div>
                    <span className="text-sm">Automated management reports</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-primary"></div>
                    <span className="text-sm">Natural language commentary</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-warning"></div>
                    <span className="text-sm">LLM-powered trend analysis</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Predictive Modeling */}
            <Card 
              className="shadow-card hover:shadow-elegant transition-all duration-300 cursor-pointer hover:scale-105"
              onClick={() => handleCardClick('/predictive-modeling')}
            >
              <CardHeader className="pb-3">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-gradient-success">
                    <TrendingUp className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <CardTitle className="text-lg">Predictive Modeling Engine</CardTitle>
                    <p className="text-sm text-muted-foreground">ML-powered forecasting models</p>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="pt-0 space-y-3">
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-accent"></div>
                    <span className="text-sm">Moving Average, Prophet & Linear</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-primary"></div>
                    <span className="text-sm">MAPE & RMSE accuracy metrics</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-warning"></div>
                    <span className="text-sm">5-year quarterly revenue analysis</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Segmentation Analysis */}
            <Card 
              className="shadow-card hover:shadow-elegant transition-all duration-300 cursor-pointer hover:scale-105"
              onClick={() => handleCardClick('/revenue-segmentation')}
            >
              <CardHeader className="pb-3">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-primary">
                    <PieChart className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <CardTitle className="text-lg">Revenue Segmentation</CardTitle>
                    <p className="text-sm text-muted-foreground">Product & segment analysis</p>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="pt-0 space-y-3">
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-accent"></div>
                    <span className="text-sm">Product segmentation breakdown</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-primary"></div>
                    <span className="text-sm">Revenue stream analysis</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-warning"></div>
                    <span className="text-sm">Market share insights</span>
                  </div>
                </div>
              </CardContent>
            </Card>

            {/* Financial News */}
            <Card 
              className="shadow-card hover:shadow-elegant transition-all duration-300 cursor-pointer hover:scale-105"
              onClick={() => handleCardClick('/market-intelligence')}
            >
              <CardHeader className="pb-3">
                <div className="flex items-center gap-3">
                  <div className="p-2 rounded-lg bg-secondary">
                    <Newspaper className="h-5 w-5 text-white" />
                  </div>
                  <div>
                    <CardTitle className="text-lg">Market Intelligence</CardTitle>
                    <p className="text-sm text-muted-foreground">Latest financial news & updates</p>
                  </div>
                </div>
              </CardHeader>
              <CardContent className="pt-0 space-y-3">
                <div className="space-y-2">
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-accent"></div>
                    <span className="text-sm">Real-time FMP articles</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-primary"></div>
                    <span className="text-sm">Market sentiment analysis</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <div className="w-1.5 h-1.5 rounded-full bg-warning"></div>
                    <span className="text-sm">Impact assessment</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* Call to Action */}
      <section className="py-8 px-6 bg-gradient-hero">
        <div className="max-w-3xl mx-auto text-center text-white">
          <h2 className="text-2xl md:text-3xl font-bold mb-3">
            Ready to Transform Your Financial Analysis?
          </h2>
          <p className="text-lg mb-6 text-white/90">
            Join the next generation of financial professionals using AI-driven insights.
          </p>
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <Button variant="financial" className="px-6">
              <Target className="mr-2 h-4 w-4" />
              Get Started Free
            </Button>
            <Button variant="outline" className="px-6 border-white text-white hover:bg-white hover:text-primary">
              <DollarSign className="mr-2 h-4 w-4" />
              Enterprise Demo
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
}