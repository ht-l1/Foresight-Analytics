"use client";

import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ReactQueryDevtools } from "@tanstack/react-query-devtools";
import { ThemeProvider } from "@/components/theme-provider";
import { type ThemeProviderProps } from "next-themes/dist/types";
import { useState } from "react";

// This declares the global variable for the browser extension to find the client
declare global {
  interface Window {
    __TANSTACK_QUERY_CLIENT__?: QueryClient;
  }
}

export function Providers({ children, ...props }: { children: React.ReactNode } & ThemeProviderProps) {
  // Create the client only once per application lifecycle
  const [queryClient] = useState(() => {
    const client = new QueryClient();
    // Connect to the DevTools extension, but only in development mode
    if (process.env.NODE_ENV === 'development') {
      window.__TANSTACK_QUERY_CLIENT__ = client;
    }
    return client;
  });

  return (
    // Provide the client to your app
    <QueryClientProvider client={queryClient}>
      {/* The original ThemeProvider */}
      <ThemeProvider {...props}>
        {children}
      </ThemeProvider>

      {/* The inline devtools for debugging */}
      <ReactQueryDevtools initialIsOpen={false} />
    </QueryClientProvider>
  );
}