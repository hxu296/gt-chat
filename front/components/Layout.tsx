import { ReactNode } from "react";

interface LayoutProps {
  children: ReactNode;
}
export default function Layout({ children }: LayoutProps) {
  return (
    <div className="flex h-full w-full flex-col items-center justify-center overflow-y-scroll bg-gray-100">
      {children}
    </div>
  );
}
