/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}"
  ],
  theme: {
    extend: {
      maxWidth: {
        fintech: "1280px"
      },

      borderRadius: {
        fintech: "14px"
      },

      boxShadow: {
        fintech: "0 2px 10px rgba(0,0,0,0.18)"
      },

      colors: {
        fintech: {
          bg: "#020617",
          card: "#0b1220",
          border: "#1e293b"
        }
      }
    }
  },
  plugins: []
}
