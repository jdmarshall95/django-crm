/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    'client/templates/client/*.html',
    'core/templates/dashboard/*.html',
    'dashboard/templates/dashboard/*.html',
    'lead/templates/lead/*.html',
    'team/templates/team/*.html',
    'userprofile/templates/userprofile/*.html',
  ],
  theme: {
    extend: {
       fontSize: {
         xs: "0.75rem",
         sm: "0.875rem",
         base: "1rem",
         lg: "1.125rem",
         xl: "1.25rem",
         "2xl": "1.5rem",
         "3xl": "1.875rem",
         "4xl": "2.25rem",
         "5xl": "3rem",
         "6xl": "4rem",
       },
    }
 },
  plugins: [],
}

