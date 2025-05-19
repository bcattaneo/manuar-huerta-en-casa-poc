<template>
    <div class="home-container">
      <!-- Cabecera con logo y título -->
      <div class="header">
        <div class="logo-container">
          <img src="@/assets/logo.png" alt="Logo Huerta en Casa" class="logo" />
        </div>
        <h1 class="text-h4 font-weight-bold text-center">Hola, ¡vamos a aprender!</h1>
      </div>
  
      <!-- TODO: Barra de búsqueda -->
      <!-- <v-sheet rounded class="mx-4 my-4 search-bar">
        <v-text-field
          density="compact"
          variant="outlined"
          prepend-inner-icon="mdi-magnify"
          placeholder="Buscar una planta..."
          hide-details
          rounded
          class="search-field"
          bg-color="accent"
        ></v-text-field>
        <v-btn icon class="menu-button" color="primary">
          <v-icon>mdi-menu</v-icon>
        </v-btn>
      </v-sheet> -->
  
      <!-- Botones principales -->
      <div class="action-buttons">
        <v-btn
          block
          color="#FFDAB9"
          height="100"
          class="identify-button"
          @click="identify"
        >
          <div class="d-flex flex-column align-center">
            <v-icon size="38" color="#A0522D">mdi-camera</v-icon>
            <span class="action-text" style="color: #A0522D">Identificar planta</span>
          </div>
        </v-btn>
  
        <v-btn
          block
          color="#FFF8DC"
          height="100"
          class="ask-button"
          @click="ask"
        >
          <div class="d-flex flex-column align-center">
            <v-icon size="38" color="#DAA520">mdi-help-circle-outline</v-icon>
            <span class="action-text" style="color: #DAA520">Preguntar</span>
          </div>
        </v-btn>
      </div>
  
      <!-- Sección de plantas del invernadero -->
      <div class="plants-section">
        <h2 class="text-h5 font-weight-medium px-4 py-3 section-title">Plantas del Invernadero</h2>
        
        <div class="plants-grid">
          <v-card
            v-for="plant in plants"
            :key="plant.id"
            class="plant-card"
            elevation="0"
            @click="openPlantDetail(plant)"
          >
            <div class="plant-image-container">
              <v-img :src="plant.image" :alt="plant.name" class="plant-image"></v-img>
            </div>
            <div class="plant-name">{{ plant.name }}</div>
          </v-card>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'HomeScreen',
    data() {
      return {
        plants: [
          { id: 1, name: 'Tomate', image: '/src/assets/plants/tomate.png' },
          { id: 2, name: 'Pepino', image: '/src/assets/plants/cucumber.png' },
        //   { id: 3, name: 'Zapallito', image: '/src/assets/plants/squash.png' },
          { id: 4, name: 'Albahaca', image: '/src/assets/plants/basil.png' },
        //   { id: 5, name: 'Tomate cherry azul', image: '/src/assets/plants/blue-tomato.png' },
        //   { id: 6, name: 'Ciboulette', image: '/src/assets/plants/chives.png' },
        ]
      }
    },
    methods: {
      identify() {
        console.log('Identificar planta')
      },
      ask() {
        console.log('Preguntar')
      },
      openPlantDetail(plant) {
        console.log('Abrir detalles de la planta:', plant.name)
      }
    }
  }
  </script>
  
  <style scoped>
  .home-container {
    max-width: 600px;
    margin: 0 auto;
    padding-bottom: 20px;
  }
  
  .header {
    padding: 20px 16px 10px;
    display: flex;
    flex-direction: column;
    align-items: center;
  }
  
  .logo-container {
    width: 50%;
    margin-bottom: 10px;
  }
  
  .logo {
    width: 100%;
    height: 100%;
  }
  
  .search-bar {
    display: flex;
    align-items: center;
    position: relative;
    background-color: #F3EFE0 !important;
  }
  
  .search-field {
    flex-grow: 1;
  }
  
  .menu-button {
    position: absolute;
    right: 5px;
  }
  
  .action-buttons {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    padding: 16px;
  }
  
  .identify-button, .ask-button {
    border-radius: 12px;
  }
  
  .action-text {
    margin-top: 8px;
    font-weight: 500;
  }
  
  .plants-section {
    background-color: #F3EFE0;
    padding-bottom: 20px;
  }
  
  .section-title {
    color: #6B8E23;
    margin: 0;
  }
  
  .plants-grid {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 8px;
    padding: 0 8px;
  }
  
  .plant-card {
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: white;
    border-radius: 12px;
    padding: 8px;
    cursor: pointer;
  }
  
  .plant-image-container {
    width: 80px;
    height: 80px;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .plant-image {
    max-width: 80%;
    max-height: 80%;
  }
  
  .plant-name {
    margin-top: 8px;
    text-align: center;
    font-size: 14px;
    color: #333;
  }
  </style>