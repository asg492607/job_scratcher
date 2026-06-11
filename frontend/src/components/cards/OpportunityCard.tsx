import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Opportunity } from '../../types/opportunity';

interface OpportunityCardProps {
  opportunity: Opportunity;
}

export const OpportunityCard: React.FC<OpportunityCardProps> = ({ opportunity }) => {
  const isNew = new Date(opportunity.created_at).getTime() > Date.now() - 3 * 24 * 60 * 60 * 1000;

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card flex flex-col h-full"
    >
      <div className="p-5 flex-1 flex flex-col">
        <div className="flex justify-between items-start mb-3 gap-3">
          <div className="flex-1 min-w-0">
            <h3 className="text-lg font-bold leading-tight mb-1 truncate" style={{ color: 'var(--text-primary)' }}>
              <Link to={`/opportunities/${opportunity.id}`} className="hover:text-transparent hover:bg-clip-text hover:bg-gradient-to-r from-purple-400 to-pink-400 transition-all duration-300">
                {opportunity.title}
              </Link>
            </h3>
            <p className="text-sm font-medium truncate" style={{ color: 'var(--text-secondary)' }}>
              {opportunity.company || 'Unknown Company'}
              {opportunity.location && (
                <>
                  {' '}
                  <span className="opacity-50 mx-1">•</span>{' '}
                  <span style={{ color: 'var(--text-muted)' }}>{opportunity.location}</span>
                </>
              )}
            </p>
          </div>
          <div className="flex flex-col items-end gap-2 flex-shrink-0">
            {isNew && (
              <span className="badge badge-new">
                <span className="w-1.5 h-1.5 rounded-full bg-pink-400 animate-pulse"></span>
                New
              </span>
            )}
          </div>
        </div>

        <div className="flex flex-wrap gap-2 mb-4">
          {opportunity.category && (
            <span className={`badge badge-${opportunity.category.replace(' ', '-')}`}>
              {opportunity.category}
            </span>
          )}
          {opportunity.remote_status && (
            <span className={`badge badge-${opportunity.remote_status}`}>
              {opportunity.remote_status}
            </span>
          )}
          {opportunity.source && (
            <span className="badge badge-source">
              <svg className="w-3 h-3 mr-0.5 opacity-70" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
              </svg>
              {opportunity.source}
            </span>
          )}
          {(opportunity.salary || opportunity.stipend) && (
            <span className="badge badge-salary">
              <svg className="w-3 h-3 mr-0.5 opacity-70" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                <path strokeLinecap="round" strokeLinejoin="round" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              {opportunity.salary || opportunity.stipend}
            </span>
          )}
        </div>

        <p className="text-sm line-clamp-3 mb-6 flex-1" style={{ color: 'var(--text-muted)' }}>
          {opportunity.description}
        </p>

        <div className="flex items-center justify-between pt-4 mt-auto border-t" style={{ borderColor: 'var(--border-light)' }}>
          <div className="flex items-center gap-1.5 flex-wrap flex-1 min-w-0 pr-4">
            {opportunity.skills && opportunity.skills.slice(0, 3).map((skill) => (
              <span key={skill.id} className="text-[10px] font-medium px-2 py-1 rounded-md" style={{ background: 'rgba(255,255,255,0.03)', color: 'var(--text-secondary)', border: '1px solid var(--border)' }}>
                {skill.name}
              </span>
            ))}
            {opportunity.skills && opportunity.skills.length > 3 && (
              <span className="text-[10px] font-medium px-2 py-1" style={{ color: 'var(--text-muted)' }}>
                +{opportunity.skills.length - 3}
              </span>
            )}
          </div>
          
          <Link
            to={`/opportunities/${opportunity.id}`}
            className="btn-outline shrink-0 flex items-center gap-2 group"
          >
            View
            <svg className="w-3.5 h-3.5 transition-transform group-hover:translate-x-0.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
              <path strokeLinecap="round" strokeLinejoin="round" d="M5 12h14M12 5l7 7-7 7" />
            </svg>
          </Link>
        </div>
      </div>
    </motion.div>
  );
};
