module.exports = {
    content: [
      './templates/**/*.html',
      './static/**/*.js',
    ],
    theme: {
      extend: {
        colors: {
          primary: '#38BDF8', // Sky blue for primary actions
          secondary: '#0284C7', // Darker sky blue for hover effects
          background: '#E0F2FE', // Light sky blue for background
          text: '#0F172A', // Dark blue for text
        },
      },
    },
    plugins: [],
};