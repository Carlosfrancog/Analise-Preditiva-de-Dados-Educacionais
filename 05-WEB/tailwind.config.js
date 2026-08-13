/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      colors: {
        sidebar:    '#0F172A',
        'sidebar-h':'#1E293B',
        accent:     '#4F46E5',
        'accent-l': '#818CF8',
        'app-bg':   '#F4F6FA',
        card:       '#FFFFFF',
        success:    '#10B981',
        warn:       '#F59E0B',
        danger:     '#EF4444',
        info:       '#0EA5E9',
        muted:      '#64748B',
        'muted-2':  '#94A3B8',
        border:     '#E5E9F0',
        'hdr-bg':   '#F8FAFC',
        'sb-text':  '#94A3B8',
        'sb-sec':   '#475569',
        text:       '#0F172A',
        'text-2':   '#1E293B',
      },
      fontFamily: {
        sans: ['"Segoe UI"', 'system-ui', 'sans-serif'],
        mono: ['"Cascadia Code"', '"Consolas"', 'monospace'],
      },
    },
  },
  plugins: [],
}
