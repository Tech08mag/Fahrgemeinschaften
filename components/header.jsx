// components/Header.js
"use client"; // needed if using Next.js 13+ app directory

import { useState } from "react";
import Link from "next/link";

export default function Header() {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen(!isMobileMenuOpen);
  };

  return (
    <header className="bg-white dark:bg-gray-800 shadow">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-4 flex items-center justify-between">
        {/* Brand */}
        <Link href="/home" className="flex items-center gap-2 text-lg sm:text-xl font-semibold text-blue-600 dark:text-blue-400">
          <img src="/static/images/Fahrgemeinschaften.png" className="w-8 h-8" alt="logo" />
          Fahrgemeinschaften
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden md:flex gap-6 text-sm font-medium">
          <Link href="/home" className="hover:text-blue-600 dark:hover:text-blue-400">Startseite</Link>
          <Link href="/mydrives" className="hover:text-blue-600 dark:hover:text-blue-400">Meine Fahrten</Link>
          <Link href="/passenger" className="hover:text-blue-600 dark:hover:text-blue-400">Mitfahrten</Link>
          <Link href="/settings" className="hover:text-blue-600 dark:hover:text-blue-400">Einstellungen</Link>
          <Link href="/logout" className="text-red-500 hover:text-red-600">ausloggen</Link>
        </nav>

        {/* Mobile Menu Button */}
        <button
          onClick={toggleMobileMenu}
          className="md:hidden text-gray-700 dark:text-gray-200"
        >
          <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h16" />
          </svg>
        </button>
      </div>

      {/* Mobile Menu */}
      {isMobileMenuOpen && (
        <div className="md:hidden bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
          <nav className="flex flex-col px-6 py-4 space-y-3 text-sm font-medium">
            <Link href="/home" className="hover:text-blue-600">Startseite</Link>
            <Link href="/mydrives" className="hover:text-blue-600">Meine Fahrten</Link>
            <Link href="/passenger" className="hover:text-blue-600 dark:hover:text-blue-400">Mitfahrten</Link>
            <Link href="/settings" className="hover:text-blue-600">Einstellungen</Link>
            <Link href="/logout" className="text-red-500 hover:text-red-600">ausloggen</Link>
          </nav>
        </div>
      )}
    </header>
  );
}
