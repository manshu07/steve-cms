/**
 * Main App Component
 */

import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { PageBuilder } from './features/page-builder';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Default route - redirect to builder with page 8 (Home) */}
        <Route path="/" element={<Navigate to="/builder/8" replace />} />

        {/* Builder route */}
        <Route
          path="/builder/:pageId"
          element={<PageBuilder pageId={8} pageName="Home" />}
        />

        {/* 404 route */}
        <Route path="*" element={<div>Page not found</div>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
