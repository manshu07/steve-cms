/**
 * Notification hook using MUI Snackbar.
 * Provides success, error, info, and warning notifications.
 */

import { useState, useCallback, createContext, useContext } from 'react';
import { Snackbar, Alert, AlertTitle } from '@mui/material';
import type { AlertColor } from '@mui/material';

interface NotificationState {
  open: boolean;
  message: string;
  severity: AlertColor;
  title?: string;
}

interface NotificationContextValue {
  showNotification: (message: string, severity?: AlertColor, title?: string) => void;
  showSuccess: (message: string, title?: string) => void;
  showError: (message: string, title?: string) => void;
  showInfo: (message: string, title?: string) => void;
  showWarning: (message: string, title?: string) => void;
}

const NotificationContext = createContext<NotificationContextValue | undefined>(undefined);

export const NotificationProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [notification, setNotification] = useState<NotificationState>({
    open: false,
    message: '',
    severity: 'info',
  });

  const showNotification = useCallback((message: string, severity: AlertColor = 'info', title?: string) => {
    setNotification({
      open: true,
      message,
      severity,
      title,
    });
  }, []);

  const showSuccess = useCallback((message: string, title?: string) => {
    showNotification(message, 'success', title);
  }, [showNotification]);

  const showError = useCallback((message: string, title?: string) => {
    showNotification(message, 'error', title);
  }, [showNotification]);

  const showInfo = useCallback((message: string, title?: string) => {
    showNotification(message, 'info', title);
  }, [showNotification]);

  const showWarning = useCallback((message: string, title?: string) => {
    showNotification(message, 'warning', title);
  }, [showNotification]);

  const handleClose = useCallback(() => {
    setNotification((prev) => ({ ...prev, open: false }));
  }, []);

  const value: NotificationContextValue = {
    showNotification,
    showSuccess,
    showError,
    showInfo,
    showWarning,
  };

  return (
    <NotificationContext.Provider value={value}>
      {children}
      <Snackbar
        open={notification.open}
        autoHideDuration={6000}
        onClose={handleClose}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert onClose={handleClose} severity={notification.severity} sx={{ width: '100%' }}>
          {notification.title && <AlertTitle>{notification.title}</AlertTitle>}
          {notification.message}
        </Alert>
      </Snackbar>
    </NotificationContext.Provider>
  );
};

export const useNotifications = (): NotificationContextValue => {
  const context = useContext(NotificationContext);
  if (!context) {
    throw new Error('useNotifications must be used within NotificationProvider');
  }
  return context;
};

export default useNotifications;
