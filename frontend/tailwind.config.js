/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Discord-inspired dark theme
        discord: {
          dark: '#1e1f22',
          darker: '#111214',
          darkest: '#060607',
          gray: '#2b2d31',
          'gray-light': '#313338',
          'gray-lighter': '#383a40',
          text: '#dbdee1',
          'text-muted': '#949ba4',
          accent: '#5865f2',
          'accent-hover': '#4752c4',
          green: '#23a559',
          yellow: '#f0b232',
          red: '#f23f43',
        }
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
      }
    },
  },
  plugins: [],
}
