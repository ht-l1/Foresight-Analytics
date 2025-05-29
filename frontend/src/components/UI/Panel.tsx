import React from 'react';

interface PanelProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  icon?: React.ReactNode;
}

const Panel: React.FC<PanelProps> = ({ children, className = '', title, icon }) => {
  return (    
    <div className={`bg-slate-800/95 backdrop-blur-md border border-slate-700/20 rounded-xl p-3 sm:p-5 shadow-2xl transition-all duration-300 hover:border-cyan-500/30 hover:shadow-cyan-500/10 hover:shadow-2xl h-full flex flex-col ${className}`}>
      {title && (
        <div className="flex items-center gap-2 mb-2 sm:mb-4 flex-shrink-0">
          {icon}
          <h3 className="text-lg sm:text-xl font-semibold text-primary-500">{title}</h3>
        </div>
      )}
      <div className="flex-1 min-h-0 overflow-auto">
        {children}
      </div>
    </div>
  );
};

export default Panel;