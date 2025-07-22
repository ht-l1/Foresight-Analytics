"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import React, { useState } from "react";
import {
  Brain,
  TrendingUp,
  PieChart,
  Newspaper,
  LayoutDashboard,
  ChevronsLeft,
} from "lucide-react";
import { cn } from "@/lib/utils";
import { Button } from "@/components/ui/button";

const navItems = [
  { href: "/", icon: LayoutDashboard, label: "Dashboard" },
  { href: "/ai-analysis", icon: Brain, label: "AI Analysis" },
  { href: "/predictive-modeling", icon: TrendingUp, label: "Predictive Modeling" },
  { href: "/revenue-segmentation", icon: PieChart, label: "Revenue Segmentation" },
  { href: "/market-intelligence", icon: Newspaper, label: "Market Intelligence" },
];

export function Sidebar() {
  const pathname = usePathname();
  const [isCollapsed, setIsCollapsed] = useState(false);

  const toggleSidebar = () => {
    setIsCollapsed(!isCollapsed);
  };

  return (
    <aside
      className={cn(
        "relative hidden h-screen border-r bg-muted/40 transition-all duration-300 ease-in-out md:flex flex-col",
        isCollapsed ? "w-20" : "w-64"
      )}
    >
      <div className="flex h-14 items-center border-b px-4 lg:h-[60px] lg:px-6">
        <Link href="/" className="flex items-center gap-2 font-semibold">
          <span className={cn(isCollapsed ? "hidden" : "block")}>Foresight</span>
        </Link>
      </div>
      <nav className="flex-1 space-y-2 px-2 py-4 lg:px-4">
        {navItems.map((item) => (
          <Link
            key={item.label}
            href={item.href}
            className={cn(
              "flex items-center gap-3 rounded-lg px-3 py-2 text-muted-foreground transition-all hover:text-primary",
              pathname === item.href && "bg-muted text-primary",
              isCollapsed && "justify-center"
            )}
          >
            <item.icon className="h-5 w-5" />
            <span className={cn("truncate", isCollapsed ? "hidden" : "block")}>
              {item.label}
            </span>
          </Link>
        ))}
      </nav>
      <div className="mt-auto p-4 border-t">
        <Button variant="ghost" size="icon" className="w-full justify-center" onClick={toggleSidebar}>
          <ChevronsLeft
            className={cn(
              "h-5 w-5 transition-transform duration-300",
              isCollapsed && "rotate-180"
            )}
          />
          <span className="sr-only">Toggle Sidebar</span>
        </Button>
      </div>
    </aside>
  );
}