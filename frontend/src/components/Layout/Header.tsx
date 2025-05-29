import React from 'react';
import { Activity, Database, TrendingUp } from 'lucide-react';

interface HeaderProps {
  modelAccuracy: number;
  isDataLive: boolean;
  isModelActive: boolean;
}

const Header: React.FC<HeaderProps> = ({ 
  modelAccuracy, 
  isDataLive, 
  isModelActive 
}) => {
  return (
    <header className="bg-dark-800/95 backdrop-blur-md border border-gray-700/20 rounded-xl p-2 sm:p-4 shadow-2xl">
      <div className="flex flex-col sm:flex-row sm:justify-between sm:items-center gap-2 sm:gap-0">
        {/* Logo Section */}
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-primary-500 to-primary-600 rounded-lg flex items-center justify-center font-bold text-white text-lg">
            FA
          </div>
          <div>
            <h1 className="text-xl font-bold text-primary-500">Foresight Analytics</h1>
            <p className="text-xs text-gray-400">ML Financial Forecasting Platform</p>
          </div>
        </div>

        {/* Status Indicators */}
        <div className="flex flex-wrap gap-2 sm:gap-4 items-center justify-center sm:justify-end">
          <div className="flex items-center gap-2 px-3 py-1 bg-primary-500/10 rounded-full">
            <div className={`w-2 h-2 rounded-full ${isModelActive ? 'bg-green-400 animate-pulse-custom' : 'bg-red-400'}`}></div>
            <span className="text-xs sm:text-sm">Model: {isModelActive ? 'Active' : 'Inactive'}</span>
          </div>
          
          <div className="flex items-center gap-2 px-3 py-1 bg-yellow-500/10 rounded-full">
            <Database className="w-3 h-3 text-yellow-400" />
            <span className="text-xs sm:text-sm">Data: {isDataLive ? 'Live' : 'Offline'}</span>
          </div>
          
          <div className="flex items-center gap-2 px-3 py-1 bg-green-500/10 rounded-full">
            <TrendingUp className="w-3 h-3 text-green-400" />
            <span className="text-xs sm:text-sm">Accuracy: {modelAccuracy.toFixed(1)}%</span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;