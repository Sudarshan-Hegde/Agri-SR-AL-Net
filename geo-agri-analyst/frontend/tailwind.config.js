/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'agri-green': '#22c55e',
        'agri-blue': '#3b82f6',
        'earth-brown': '#a3765a',
      }
    },
  },
  plugins: [],
}