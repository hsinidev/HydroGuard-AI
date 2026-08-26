/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        scada: {
          bg: '#080c16',
          card: '#0f172a',
          border: '#1e293b',
          cyan: '#06b6d4'
        }
      }
    },
  },
  plugins: [],
}
