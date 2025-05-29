/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f9ff',
          500: '#00d4ff',
          600: '#0099cc',
          700: '#0077aa',
          900: '#0f0f23',
        },
        dark: {
          100: '#e0e0e0',
          200: '#b0b0b0',
          300: '#888',
          800: '#1a1a2e',
          900: '#0f0f23',
        },
        slate: {
          800: '#1a1a2e',
          900: '#0f0f23',
        },
      },
      backdropBlur: {
        xs: '2px',
      },
    },
  },
  plugins: [],
}