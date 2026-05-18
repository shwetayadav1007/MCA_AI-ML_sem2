export default {
  content: ['./index.html', './src/**/*.{js,jsx}'],
  theme: {
    extend: {
      boxShadow: {
        glow: '0 20px 60px rgba(14, 165, 233, 0.18)',
      },
      backgroundImage: {
        'hero-gradient': 'radial-gradient(circle at top, rgba(56,189,248,0.35), transparent 35%), linear-gradient(135deg, #0ea5e9 0%, #0284c7 100%)',
      },
    },
  },
  plugins: [],
}
