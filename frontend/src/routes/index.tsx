import { Routes, Route, Navigate } from 'react-router-dom';
import { MainLayout } from '../components/layout/MainLayout';
import { DiscoveryPage } from '../features/opportunities/DiscoveryPage';
import { DetailsPage } from '../features/opportunities/DetailsPage';

export function AppRoutes() {
  return (
    <Routes>
      <Route path="/" element={<MainLayout />}>
        <Route index element={<Navigate to="/opportunities" replace />} />
        <Route path="opportunities" element={<DiscoveryPage />} />
        <Route path="opportunities/:id" element={<DetailsPage />} />
        <Route path="*" element={<Navigate to="/opportunities" replace />} />
      </Route>
    </Routes>
  );
}
