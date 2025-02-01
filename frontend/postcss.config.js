// postcss.config.js
module.exports = {
  plugins: [
    require('@tailwindcss/postcss'), // Asegúrate de usar el plugin correcto
    require('autoprefixer'), // También aseguramos que autoprefixer esté presente
  ],
}
