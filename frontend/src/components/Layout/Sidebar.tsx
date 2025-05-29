import React, { useState } from 'react';
import { Filter, Settings, Play, Download, Wrench } from 'lucide-react';

interface SidebarProps {
  onFilterChange: (filters: any) => void;
  onForecastRun: () => void;
  onExportResults: () => void;
  isLoading?: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({ 
  onFilterChange, 
  onForecastRun, 
  onExportResults,
  isLoading = false 
}) => {
  const [filters, setFilters] = useState({
    region: 'All',
    category: 'All',
    modelType: 'Linear Regression',
    forecastHorizon: 6,
    confidenceLevel: '95%'
  });

  const handleFilterChange = (key: string, value: any) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    onFilterChange(newFilters);
  };

  return (
    <aside className="bg-dark-800/95 backdrop-blur-md border border-gray-700/20 rounded-xl p-2 sm:p-4 shadow-2xl space-y-2 sm:space-y-4 h-full overflow-y-auto">
      {/* Data Filters Section */}
      <div className="bg-dark-900/60 p-2 sm:p-3 rounded-lg border-l-4 border-primary-500">
        <div className="flex items-center gap-2 mb-3">
          <Filter className="w-4 h-4 text-primary-500" />
          <h3 className="text-primary-500 font-semibold text-sm">Data Filters</h3>
        </div>
        
        <div className="space-y-3">
          <div>
            <label className="block text-xs font-medium text-gray-300 mb-1">Region</label>
            <select 
              className="w-full p-2 bg-dark-900/80 border border-gray-600/30 rounded-lg text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              value={filters.region}
              onChange={(e) => handleFilterChange('region', e.target.value)}
            >
              <option>All</option>
              <option>South</option>
              <option>West</option>
              <option>North</option>
              <option>East</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-300 mb-1">Category</label>
            <select 
              className="w-full p-2 bg-dark-900/80 border border-gray-600/30 rounded-lg text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              value={filters.category}
              onChange={(e) => handleFilterChange('category', e.target.value)}
            >
              <option>All</option>
              <option>Furniture</option>
              <option>Office Supplies</option>
              <option>Technology</option>
            </select>
          </div>
        </div>
      </div>

      {/* ML Parameters Section */}
      <div className="bg-purple-900/20 p-2 sm:p-3 rounded-lg border-l-4 border-red-400">
        <div className="flex items-center gap-2 mb-3">
          <Settings className="w-4 h-4 text-red-400" />
          <h3 className="text-red-400 font-semibold text-sm">ML Parameters</h3>
        </div>
        
        <div className="space-y-3">
          <div>
            <label className="block text-xs font-medium text-gray-300 mb-1">Model Type</label>
            <select 
              className="w-full p-2 bg-dark-900/80 border border-gray-600/30 rounded-lg text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              value={filters.modelType}
              onChange={(e) => handleFilterChange('modelType', e.target.value)}
            >
              <option>Linear Regression</option>
              <option>Random Forest</option>
              <option>ARIMA</option>
              <option>LSTM</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-300 mb-1">
              Forecast Horizon: {filters.forecastHorizon} months
            </label>
            <input 
              type="range" 
              min="1" 
              max="48" 
              value={filters.forecastHorizon}
              onChange={(e) => handleFilterChange('forecastHorizon', parseInt(e.target.value))}
              className="w-full h-2 bg-dark-900 rounded-lg appearance-none cursor-pointer slider"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-gray-300 mb-1">Confidence Level</label>
            <select 
              className="w-full p-2 bg-dark-900/80 border border-gray-600/30 rounded-lg text-gray-100 text-sm focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              value={filters.confidenceLevel}
              onChange={(e) => handleFilterChange('confidenceLevel', e.target.value)}
            >
              <option>95%</option>
              <option>90%</option>
              <option>80%</option>
            </select>
          </div>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="space-y-2">
        <button 
          onClick={onForecastRun}
          disabled={isLoading}
          className="w-full flex items-center justify-center gap-2 p-2 bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 text-white rounded-lg font-semibold text-sm transition-all duration-200 transform hover:-translate-y-1 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <Play className="w-4 h-4" />
          {isLoading ? 'Running...' : 'Run Forecast'}
        </button>
        
        <button 
          onClick={onExportResults}
          className="w-full flex items-center justify-center gap-2 p-2 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 text-white rounded-lg font-medium text-sm transition-all duration-200 transform hover:-translate-y-1"
        >
          <Download className="w-4 h-4" />
          Export Results
        </button>
        
        <button className="w-full flex items-center justify-center gap-2 p-2 bg-gradient-to-r from-gray-600 to-gray-700 hover:from-gray-700 hover:to-gray-800 text-white rounded-lg font-medium text-sm transition-all duration-200 transform hover:-translate-y-1">
          <Wrench className="w-4 h-4" />
          Tune Model
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;