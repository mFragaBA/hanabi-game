const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
    	backgroundImage: theme => ({
		'hanabi': "url('./img/hanabi.png')",
		'dorso': "url('./img/dorso.svg')",
	}),
	backgroundColor: theme => ({
		'carta': '#41437a',
	}),
	fontFamily: {
		'cursive': ['"Comic Sans MS"'],
	},
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
