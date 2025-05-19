// src/plugins/vuetify.js
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'

const customTheme = {
  dark: false,
  colors: {
    primary: '#6B8E23', // Verde oliva - color principal
    secondary: '#8FBC8F', // Verde mar - color secundario
    accent: '#F3EFE0', // Crema suave - color de acento
    background: '#F9F9F5', // Fondo claro
    error: '#FF5252', // Rojo para errores
    info: '#2196F3', // Azul para información
    success: '#81C784', // Verde éxito
    warning: '#FFC107' // Amarillo advertencia
  }
}

export default createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'customTheme',
    themes: {
      customTheme
    }
  },
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
})