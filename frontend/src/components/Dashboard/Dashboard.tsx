import React, { useState, useEffect } from 'react';
import Header from '../Layout/Header';
import Sidebar from '../Layout/Sidebar';
import Panel from '../UI/Panel';
import { 
  TrendingUp, 
  BarChart3, 
  Brain, 
  FileText, 
  AlertTriangle,
  Activity,
  Target
} from 'lucide-react';

const Dashboard: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [filters, setFilters] = useState({ region: 'All', category: 'All' });
  const [dashboardData, setDashboardData] = useState({
    modelAccuracy: 85.0,
    isDataLive: true,
    isModelActive: true,
  });

  const handleFilterChange = (newFilters: any) => {
    setFilters(newFilters);
    console.log('Filters updated:', newFilters);
  };

  const handleForecastRun = async () => {
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      console.log('Forecast completed');
    }, 2000);
  };

  const handleExportResults = () => {
    console.log('Exporting results...');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <div className="dashboard-grid">
        {/* Header */}
        <div className="grid-area-header">
          <Header 
            modelAccuracy={dashboardData.modelAccuracy}
            isDataLive={dashboardData.isDataLive}
            isModelActive={dashboardData.isModelActive}
          />
        </div>

        {/* Sidebar */}
        <div className="grid-area-sidebar">
          <Sidebar 
            onFilterChange={handleFilterChange}
            onForecastRun={handleForecastRun}
            onExportResults={handleExportResults}
            isLoading={isLoading}
          />
        </div>

        {/* Main Forecast Chart */}
        <div className="grid-area-main-forecast">
          <Panel 
            title="Sales Forecast" 
            icon={<TrendingUp className="w-[1.25rem] h-[1.25rem] text-cyan-400" />}
          >
            <div className="flex justify-between items-center mb-[0.75rem]">
              <span className="text-cyan-400 bg-cyan-500/10 px-[0.5rem] py-[0.25rem] rounded-full text-[0.75rem]">
                Next 6 Months
              </span>
            </div>
            <div className="flex-1 bg-slate-900/50 rounded-lg border-2 border-dashed border-gray-600/30 flex items-center justify-center">
              <div className="text-center text-gray-400">
                <BarChart3 className="w-[2rem] h-[2rem] mx-auto mb-[0.5rem] opacity-50" />
                <p className="text-[0.875rem]">📈 Interactive Forecast Chart</p>
                <p className="text-[0.75rem]">Historical vs Predicted with Confidence Intervals</p>
              </div>
            </div>
          </Panel>
        </div>

        {/* Model Performance */}
        <div className="grid-area-model-performance">
          <Panel 
            title="Model Performance" 
            icon={<Target className="w-[1.25rem] h-[1.25rem] text-cyan-400" />}
          >
            <div className="grid grid-cols-2 gap-[0.5rem] mb-[1rem]">
              <div className="bg-slate-900/60 p-[0.5rem] rounded-lg border-t-2 border-cyan-500 text-center">
                <div className="text-[1.125rem] font-bold text-cyan-400">Linear Regression</div>
                <div className="text-[0.75rem] text-gray-400 uppercase">Current Model</div>
              </div>
              <div className="bg-slate-900/60 p-[0.5rem] rounded-lg border-t-2 border-green-400 text-center">
                <div className="text-[1.125rem] font-bold text-green-400">85.0%</div>
                <div className="text-[0.75rem] text-gray-400 uppercase">Accuracy</div>
              </div>
              <div className="bg-slate-900/60 p-[0.5rem] rounded-lg border-t-2 border-red-400 text-center">
                <div className="text-[1.125rem] font-bold text-red-400">4.5%</div>
                <div className="text-[0.75rem] text-gray-400 uppercase">MAPE</div>
              </div>
              <div className="bg-slate-900/60 p-[0.5rem] rounded-lg border-t-2 border-yellow-400 text-center">
                <div className="text-[1.125rem] font-bold text-yellow-400">0.87</div>
                <div className="text-[0.75rem] text-gray-400 uppercase">R² Score</div>
              </div>
            </div>
          </Panel>
        </div>

        {/* Model Comparison */}
        <div className="grid-area-model-comparison">
          <Panel 
            title="Model Comparison" 
            icon={<Target className="w-[1.25rem] h-[1.25rem] text-cyan-400" />}
          >
            <div className="bg-slate-900/30 p-[0.75rem] rounded-lg">
              <h4 className="text-cyan-400 font-semibold mb-[0.5rem] text-[0.875rem]">Comparison</h4>
              <div className="space-y-[0.25rem]">
                {[
                  { name: '🏆 Linear Regression', score: '85.0%' },
                  { name: 'Random Forest', score: '82.5%' },
                  { name: 'ARIMA', score: '80.0%' },
                  { name: 'LSTM', score: '81.2%' }
                ].map((model, idx) => (
                  <div key={idx} className="flex justify-between items-center py-[0.25rem] border-b border-gray-700/30">
                    <span className="text-[0.75rem]">{model.name}</span>
                    <span className="text-green-400 font-semibold text-[0.75rem]">{model.score}</span>
                  </div>
                ))}
              </div>
            </div>
          </Panel>
        </div>

        {/* Forecast Results */}
        <div className="grid-area-forecast-results">
          <Panel 
            title="Forecast Results" 
            icon={<FileText className="w-[1.25rem] h-[1.25rem] text-cyan-400" />}
          >
            <div className="grid grid-cols-2 gap-[0.5rem] mb-[0.75rem]">
              <div className="bg-slate-900/60 p-[0.5rem] rounded-lg text-center">
                <div className="text-[1.125rem] font-bold text-green-400">$500K</div>
                <div className="text-[0.75rem] text-gray-400">Predicted Total</div>
              </div>
              <div className="bg-slate-900/60 p-[0.5rem] rounded-lg text-center">
                <div className="text-[1.125rem] font-bold text-green-400">+10%</div>
                <div className="text-[0.75rem] text-gray-400">Growth Rate</div>
              </div>
            </div>
            
            <div className="bg-slate-900/30 rounded-lg p-[0.5rem] max-h-[8rem] overflow-y-auto">
              <div className="grid grid-cols-3 gap-[0.25rem] text-[0.75rem] font-semibold text-cyan-400 mb-[0.25rem] pb-[0.25rem] border-b border-cyan-500/30">
                <div>Month</div>
                <div>Prediction</div>
                <div>Confidence</div>
              </div>
              {[
                { month: 'Jun 2025', pred: '$450K', conf: '±5%' },
                { month: 'Jul 2025', pred: '$460K', conf: '±6%' },
                { month: 'Aug 2025', pred: '$470K', conf: '±7%' },
                { month: 'Sep 2025', pred: '$480K', conf: '±8%' },
                { month: 'Oct 2025', pred: '$490K', conf: '±9%' },
                { month: 'Nov 2025', pred: '$500K', conf: '±10%' },
              ].map((row, idx) => (
                <div key={idx} className="grid grid-cols-3 gap-[0.25rem] text-[0.75rem] py-[0.25rem] border-b border-gray-700/20">
                  <div className="text-gray-300">{row.month}</div>
                  <div className="text-white">{row.pred}</div>
                  <div className="text-gray-400">{row.conf}</div>
                </div>
              ))}
            </div>
          </Panel>
        </div>

        {/* AI Insights */}
        <div className="grid-area-ai-insights">
          <Panel 
            title="AI Insights" 
            icon={<Brain className="w-[1.25rem] h-[1.25rem] text-cyan-400" />}
          >
            <div className="space-y-[0.5rem]">
              <div className="bg-green-900/20 border-l-2 border-green-400 p-[0.5rem] rounded">
                <div className="text-[0.75rem] text-gray-300">Under Development</div>
              </div>
            </div>
          </Panel>
        </div>

        {/* System Alerts */}
        <div className="grid-area-system-alerts">
          <Panel 
            title="System Alerts" 
            icon={<AlertTriangle className="w-[1.25rem] h-[1.25rem] text-red-400" />}
          >
            <div className="space-y-[0.5rem]">
              <div className="bg-yellow-900/20 border-l-2 border-yellow-400 p-[0.5rem] rounded">
                <div className="text-[0.75rem] text-gray-300">Under Development</div>
              </div>
            </div>
          </Panel>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;