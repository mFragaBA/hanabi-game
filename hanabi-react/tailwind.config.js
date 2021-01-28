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
	boxShadow: {
		red: '0 35px 60px -15px rgba(242, 217, 132, 0.6)',
	},
    },
  },
  variants: {
    extend: {
      zIndex: ['hover'],
      backgroundColor: ['even', 'odd'],
    },
  },
  plugins: [],
}
