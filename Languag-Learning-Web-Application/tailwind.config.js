/** @type {import('tailwindcss').Config} */
module.exports = {
  // filepath for all jsx css html files
  content: [
    './src/login.jsx',
    './src/register.jsx',
    './src/**/*.{html,js,jsx}',
    './pages/**/*.{html,js}',
    './components/**/*.{html,js}',
    './layouts/**/*.{html,js}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

