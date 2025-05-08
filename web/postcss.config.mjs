export default {
    plugins: {
        "@tailwindcss/postcss": {},
        autoprefixer: {},
    },
    theme: {
        extend: {
            gridTemplateColumns: {
                '24': 'repeat(24, minmax(0, 1fr))',
            }
        }
    }
};