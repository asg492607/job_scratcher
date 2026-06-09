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
      whileHover={{ y: -2, boxShadow: '0 10px 25px -5px rgba(0, 0, 0, 0.05), 0 8px 10px -6px rgba(0, 0, 0, 0.01)' }}
      className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm transition-all duration-200"
    >
      <div className="p-5">
        <div className="flex justify-between items-start mb-3">
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-slate-900 leading-tight mb-1">
              <Link to={`/opportunities/${opportunity.id}`} className="hover:text-indigo-600 transition-colors">
                {opportunity.title}
              </Link>
            </h3>
            <p className="text-sm text-slate-600 font-medium">
              {opportunity.company || 'Unknown company'}
              {opportunity.location && (
                <>
                  {' '}&bull; <span className="text-slate-500">{opportunity.location}</span>
                </>
              )}
            </p>
          </div>
          <div className="flex flex-col items-end space-y-2">
            {isNew && (
              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-indigo-50 text-indigo-700">
                New
              </span>
            )}
            {opportunity.source && (
              <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-medium bg-slate-50 text-slate-600">
                {opportunity.source}
              </span>
            )}
          </div>
        </div>

        <div className="flex flex-wrap gap-2 mb-4">
          {opportunity.category && (
            <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium bg-slate-100 text-slate-700 capitalize">
              {opportunity.category}
            </span>
          )}
          {opportunity.remote_status && (
            <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium bg-slate-100 text-slate-700 capitalize">
              {opportunity.remote_status}
            </span>
          )}
          {(opportunity.salary || opportunity.stipend) && (
            <span className="inline-flex items-center px-2.5 py-1 rounded-md text-xs font-medium bg-green-50 text-green-700">
              {opportunity.salary || opportunity.stipend}
            </span>
          )}
        </div>

        <p className="text-sm text-slate-600 line-clamp-2 mb-4">
          {opportunity.description}
        </p>

        <div className="flex items-center justify-between mt-4 pt-4 border-t border-slate-100">
          <div className="flex items-center space-x-2 text-xs text-slate-500">
            {opportunity.skills && opportunity.skills.slice(0, 3).map((skill, index) => (
              <span key={skill.id} className="truncate">
                {skill.name}{index < Math.min(opportunity.skills!.length, 3) - 1 ? ',' : ''}
              </span>
            ))}
            {opportunity.skills && opportunity.skills.length > 3 && (
              <span>+{opportunity.skills.length - 3} more</span>
            )}
          </div>
          <Link
            to={`/opportunities/${opportunity.id}`}
            className="inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-colors"
          >
            View Details
          </Link>
        </div>
      </div>
    </motion.div>
  );
};
