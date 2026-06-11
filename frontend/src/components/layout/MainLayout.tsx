import { Outlet, Link, useLocation } from 'react-router-dom';

export function MainLayout() {
  const location = useLocation();

  return (
    <div className="min-h-screen relative" style={{ background: 'var(--bg-primary)' }}>
      {/* Background orbs */}
      <div className="bg-orb w-[600px] h-[600px] top-[-200px] left-[-200px]"
        style={{ background: 'radial-gradient(circle, rgba(124,58,237,0.25) 0%, transparent 70%)' }} />
      <div className="bg-orb w-[500px] h-[500px] top-[30%] right-[-150px]"
        style={{ background: 'radial-gradient(circle, rgba(236,72,153,0.15) 0%, transparent 70%)' }} />
      <div className="bg-orb w-[400px] h-[400px] bottom-0 left-[30%]"
        style={{ background: 'radial-gradient(circle, rgba(6,182,212,0.1) 0%, transparent 70%)' }} />

      {/* Nav */}
      <header className="relative z-20 sticky top-0"
        style={{ background: 'rgba(10,10,15,0.85)', backdropFilter: 'blur(24px)', borderBottom: '1px solid var(--border)' }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          {/* Logo */}
          <Link to="/opportunities" className="flex items-center gap-3 group">
            <div className="w-8 h-8 rounded-lg flex items-center justify-center relative overflow-hidden"
              style={{ background: 'linear-gradient(135deg, #7c3aed, #ec4899)' }}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5" stroke="white" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
            </div>
            <div>
              <span className="font-bold text-lg tracking-tight" style={{ fontFamily: 'Syne, sans-serif', color: 'var(--text-primary)' }}>
                Design<span className="gradient-text">Scout</span>
              </span>
              <div className="text-[10px] font-medium" style={{ color: 'var(--text-muted)', lineHeight: 1, marginTop: -2 }}>
                Opportunity Intelligence
              </div>
            </div>
          </Link>

          {/* Nav links */}
          <nav className="hidden md:flex items-center gap-1">
            {[
              { to: '/opportunities', label: 'Discover', icon: '🔭' },
            ].map(({ to, label, icon }) => (
              <Link key={to} to={to}
                className="flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all duration-200"
                style={{
                  color: location.pathname.startsWith(to) ? 'var(--text-primary)' : 'var(--text-secondary)',
                  background: location.pathname.startsWith(to) ? 'rgba(124,58,237,0.12)' : 'transparent',
                  border: location.pathname.startsWith(to) ? '1px solid rgba(124,58,237,0.2)' : '1px solid transparent',
                }}>
                <span>{icon}</span>
                {label}
              </Link>
            ))}
          </nav>

          {/* Right side */}
          <div className="flex items-center gap-3">
            <a href="https://github.com/asg492607/job_scratcher" target="_blank" rel="noopener noreferrer"
              className="hidden md:flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-medium transition-all"
              style={{ color: 'var(--text-muted)', border: '1px solid var(--border)' }}>
              <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C6.477 2 2 6.477 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.09-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0012 2z"/>
              </svg>
              Source
            </a>
          </div>
        </div>
      </header>

      {/* Page content */}
      <main className="relative z-10">
        <Outlet />
      </main>

      {/* Footer */}
      <footer className="relative z-10 mt-20 border-t" style={{ borderColor: 'var(--border)', background: 'rgba(10,10,15,0.7)' }}>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded-md" style={{ background: 'linear-gradient(135deg, #7c3aed, #ec4899)' }} />
            <span className="text-sm font-semibold" style={{ color: 'var(--text-secondary)' }}>DesignScout</span>
          </div>
          <p className="text-xs" style={{ color: 'var(--text-muted)' }}>
            Aggregating opportunities from LinkedIn, Behance, Dribbble, Internshala & 15+ platforms
          </p>
          <p className="text-xs" style={{ color: 'var(--text-muted)' }}>Built for design students ✦</p>
        </div>
      </footer>
    </div>
  );
}
