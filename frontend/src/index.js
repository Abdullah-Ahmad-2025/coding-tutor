import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

// ============================================================
// COMPLETE RESIZEOBSERVER ERROR SUPPRESSION
// ============================================================

// 1. Override console.error to filter ResizeObserver
const originalConsoleError = console.error;
console.error = function (...args) {
  const message = args[0];
  if (typeof message === 'string' && message.includes('ResizeObserver')) {
    return; // Silently ignore
  }
  // Also check if any argument is an Error with ResizeObserver
  if (args.some(arg => arg instanceof Error && arg.message?.includes?.('ResizeObserver'))) {
    return;
  }
  originalConsoleError.apply(console, args);
};

// 2. Override window.onerror
const originalOnError = window.onerror;
window.onerror = function (message, source, lineno, colno, error) {
  if (typeof message === 'string' && message.includes('ResizeObserver')) {
    return true; // Suppress
  }
  if (error?.message?.includes?.('ResizeObserver')) {
    return true;
  }
  if (originalOnError) {
    return originalOnError(message, source, lineno, colno, error);
  }
  return false;
};

// 3. Intercept error events
window.addEventListener('error', function (e) {
  if (e.message && e.message.includes('ResizeObserver')) {
    e.stopImmediatePropagation();
    e.preventDefault();
    return true;
  }
}, true); // Using capture phase

// 4. Intercept unhandledrejection events
window.addEventListener('unhandledrejection', function (e) {
  if (e.reason?.message?.includes?.('ResizeObserver')) {
    e.preventDefault();
    e.stopPropagation();
    return true;
  }
});

// 5. Monkey patch ResizeObserver to prevent loop errors
// This is the nuclear option – prevents ResizeObserver from throwing
if (window.ResizeObserver) {
  const OriginalResizeObserver = window.ResizeObserver;
  window.ResizeObserver = function (callback) {
    const wrappedCallback = function (entries, observer) {
      try {
        callback(entries, observer);
      } catch (e) {
        if (e.message && e.message.includes('ResizeObserver')) {
          // Swallow the error silently
        } else {
          throw e;
        }
      }
    };
    return new OriginalResizeObserver(wrappedCallback);
  };
  // Copy prototype methods
  window.ResizeObserver.prototype = OriginalResizeObserver.prototype;
}

// ============================================================

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

reportWebVitals();