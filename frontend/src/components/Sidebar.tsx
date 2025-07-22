"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Brain, TrendingUp, PieChart, Newspaper } from "lucide-react";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/ai-analysis", icon: Brain, label: "AI Analysis" },
  { href: "/predictive-modeling", icon: TrendingUp, label: "Predictive Modeling" },
  { href: "/revenue-segmentation", icon: PieChart, label: "Revenue Segmentation" },
  { href: "/market-intelligence", icon: Newspaper, label: "Market Intelligence" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 bg-sidebar text-sidebar-foreground p-4">
      <div className="mb-8">
        <Link href="/" className="text-2xl font-bold text-sidebar-primary">
          Foresight
        </Link>
      </div>
      <nav>
        <ul>
          {navItems.map((item) => (
            <li key={item.href}>
              <Link
                href={item.href}
                className={cn(
                  "flex items-center p-2 rounded-md transition-colors",
                  pathname === item.href
                    ? "bg-sidebar-primary text-sidebar-primary-foreground"
                    : "hover:bg-sidebar-accent"
                )}
              >
                <item.icon className="w-5 h-5 mr-3" />
                {item.label}
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
}