"use client";

import { QueryClient, QueryClientProvider } from "react-query";
import { ThemeProvider } from "@/components/theme-provider";
import { type ThemeProviderProps } from "next-themes/dist/types";
import { useState } from "react";

export function Providers({ children, ...props }: { children: React.ReactNode } & ThemeProviderProps) {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider {...props}>{children}</ThemeProvider>
    </QueryClientProvider>
  );
}