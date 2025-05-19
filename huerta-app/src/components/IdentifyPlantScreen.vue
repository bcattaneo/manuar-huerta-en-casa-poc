<template>
    <div class="identify-container">
      <!-- Barra superior con botón de volver -->
      <div class="identify-header">
        <v-btn
          variant="text"
          density="comfortable"
          icon="mdi-chevron-left"
          color="#6B8E23"
          @click="goBack"
        >
        </v-btn>
        <span class="identify-title">Identificar planta</span>
      </div>
  
      <!-- Área principal de la cámara/visualización -->
      <div class="camera-container">
        <!-- Vista previa de la cámara cuando está activa -->
        <video 
          v-if="isCameraActive && !capturedImage" 
          ref="cameraPreview" 
          class="camera-preview" 
          autoplay 
          playsinline
        ></video>
        
        <!-- Imagen capturada cuando está disponible -->
        <img 
          v-if="capturedImage" 
          :src="capturedImage" 
          class="captured-image" 
          alt="Imagen capturada"
        />
        
        <!-- Overlay de análisis cuando está procesando -->
        <div v-if="isAnalyzing" class="analysis-overlay">
          <v-progress-circular
            indeterminate
            color="#6B8E23"
            size="64"
          ></v-progress-circular>
          <div class="analysis-text">Analizando planta...</div>
        </div>
        
        <!-- Mensaje cuando la cámara no está disponible -->
        <div v-if="!isCameraActive && !capturedImage" class="camera-placeholder">
          <v-icon size="64" color="grey-darken-1">mdi-camera-off</v-icon>
          <div class="placeholder-text">
            {{ cameraErrorMessage || "Toca para activar la cámara" }}
          </div>
        </div>
      </div>
  
      <!-- Controles de la cámara -->
      <div class="camera-controls">
        <template v-if="!capturedImage">
          <!-- Botón para activar la cámara si no está activa -->
          <v-btn
            v-if="!isCameraActive"
            color="#6B8E23"
            variant="elevated"
            rounded
            size="large"
            @click="startCamera"
          >
            <v-icon left>mdi-camera</v-icon>
            Activar cámara
          </v-btn>
          
          <!-- Botón para capturar foto si la cámara está activa -->
          <v-btn
            v-else
            color="#6B8E23"
            variant="elevated"
            icon
            size="x-large"
            class="capture-btn"
            @click="captureImage"
          >
            <v-icon size="36">mdi-camera</v-icon>
          </v-btn>
        </template>
        
        <!-- Botones después de capturar la imagen -->
        <template v-else>
          <div class="post-capture-controls">
            <v-btn
              color="error"
              variant="elevated"
              rounded
              @click="resetCamera"
            >
              <v-icon left>mdi-camera-retake</v-icon>
              Repetir
            </v-btn>
            
            <v-btn
              color="#6B8E23"
              variant="elevated"
              rounded
              @click="identifyPlant"
              :disabled="isAnalyzing"
            >
              <v-icon left>mdi-leaf</v-icon>
              Identificar
            </v-btn>
          </div>
        </template>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'IdentifyPlantScreen',
    data() {
      return {
        isCameraActive: false,
        capturedImage: null,
        isAnalyzing: false,
        stream: null,
        cameraErrorMessage: '',
        // Mock de respuestas para simular la API
        mockIdentifications: [
          { imagePattern: 'red', plantName: 'Tomate' },
          { imagePattern: 'green', plantName: 'Pepino' },
          { imagePattern: 'round', plantName: 'Zapallito' },
          { imagePattern: 'leaf', plantName: 'Albahaca' },
          { imagePattern: 'blue', plantName: 'Tomate cherry azul' },
          { imagePattern: 'thin', plantName: 'Ciboulette' },
        ]
      };
    },
    beforeUnmount() {
      this.stopCamera();
    },
    methods: {
      goBack() {
        this.stopCamera();
        this.$router.go(-1);
      },
      
      async startCamera() {
        try {
          // Solicitar acceso a la cámara trasera (preferiblemente)
          this.stream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode: 'environment' },
            audio: false
          });
          
          // Establecer la vista previa de la cámara
          if (this.$refs.cameraPreview) {
            this.$refs.cameraPreview.srcObject = this.stream;
          }
          
          this.isCameraActive = true;
          this.cameraErrorMessage = '';
        } catch (error) {
          console.error('Error al acceder a la cámara:', error);
          this.cameraErrorMessage = 'No se pudo acceder a la cámara. Verifica los permisos.';
          
          // Si hay un error con la cámara trasera, intentar con la frontal
          try {
            this.stream = await navigator.mediaDevices.getUserMedia({
              video: true,
              audio: false
            });
            
            if (this.$refs.cameraPreview) {
              this.$refs.cameraPreview.srcObject = this.stream;
            }
            
            this.isCameraActive = true;
            this.cameraErrorMessage = '';
          } catch (secondError) {
            console.error('Error al acceder a cualquier cámara:', secondError);
            this.cameraErrorMessage = 'No se pudo acceder a ninguna cámara. Verifica los permisos.';
          }
        }
      },
      
      stopCamera() {
        if (this.stream) {
          this.stream.getTracks().forEach(track => track.stop());
          this.stream = null;
        }
        this.isCameraActive = false;
      },
      
      captureImage() {
        if (!this.isCameraActive) return;
        
        const video = this.$refs.cameraPreview;
        const canvas = document.createElement('canvas');
        
        // Configurar el canvas con las dimensiones del video
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        // Dibujar el frame actual del video en el canvas
        const context = canvas.getContext('2d');
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // Convertir a base64
        this.capturedImage = canvas.toDataURL('image/jpeg');
        console.log(this.capturedImage);
        
        // Opcional: detener la cámara después de capturar
        this.stopCamera();
      },
      
      resetCamera() {
        this.capturedImage = null;
        this.isAnalyzing = false;
        this.startCamera();
      },
      
      identifyPlant() {
        if (!this.capturedImage) return;
        
        this.isAnalyzing = true;
        
        // Simular una llamada a la API con un tiempo de espera
        setTimeout(() => {
          // En una implementación real, aquí enviarías la imagen a la API
          // const imageData = this.capturedImage.split(',')[1]; // Obtener datos base64 sin el prefijo
          
          // Simular una respuesta de la API basada en colores aleatorios en la imagen
          const identifiedPlant = this.mockIdentifyPlant(this.capturedImage);
          
          // Finalizar el análisis
          this.isAnalyzing = false;
          
          // Navegar a la pantalla de chat con la planta identificada
          this.$router.push({
            path: '/chat',
            query: { plant: identifiedPlant }
          });
        }, 2000); // Simular un retraso de 2 segundos
      },
      
      mockIdentifyPlant(imageData) {
        // En un escenario real, esto sería reemplazado por la respuesta de la API
        
        // Implementación simple: devolver una planta aleatoria del mock
        // En una app real, analizarías la imagen o llamarías a una API
        const randomIndex = Math.floor(Math.random() * this.mockIdentifications.length);
        return this.mockIdentifications[randomIndex].plantName;
        
        /* 
        // Para una versión más avanzada, podrías analizar la imagen
        // y buscar coincidencias de color, forma, etc.
        const colorAnalysis = this.analyzeImageColors(imageData);
        
        // Buscar coincidencia en el mock basado en el análisis
        for (const identification of this.mockIdentifications) {
          if (colorAnalysis.includes(identification.imagePattern)) {
            return identification.plantName;
          }
        }
        
        // Si no hay coincidencia, devolver una planta por defecto
        return 'Planta Desconocida';
        */
      },
      
      /* 
      // Método para un análisis simple de colores (no implementado)
      analyzeImageColors(imageData) {
        // Implementación simple para demostración
        // En una app real, usarías una biblioteca de procesamiento de imagen
        return ['green']; // Valor de ejemplo
      }
      */
    }
  };
  </script>
  
  <style scoped>
  .identify-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    max-width: 600px;
    margin: 0 auto;
    background-color: #F3F3F3;
  }
  
  .identify-header {
    display: flex;
    align-items: center;
    padding: 10px 16px;
    background-color: white;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    z-index: 10;
  }
  
  .identify-title {
    margin-left: 10px;
    font-size: 18px;
    font-weight: 500;
    color: #333;
  }
  
  .camera-container {
    flex: 1;
    position: relative;
    overflow: hidden;
    background-color: #000;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .camera-preview, .captured-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }
  
  .camera-placeholder {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    width: 100%;
    height: 100%;
    background-color: #333;
    color: white;
    text-align: center;
    padding: 20px;
  }
  
  .placeholder-text {
    margin-top: 16px;
    font-size: 18px;
  }
  
  .analysis-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.7);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    z-index: 20;
  }
  
  .analysis-text {
    margin-top: 20px;
    color: white;
    font-size: 18px;
    font-weight: 500;
  }
  
  .camera-controls {
    padding: 20px;
    display: flex;
    justify-content: center;
    background-color: #F3F3F3;
  }
  
  .capture-btn {
    height: 70px;
    width: 70px;
    border-radius: 50%;
  }
  
  .post-capture-controls {
    display: flex;
    justify-content: space-between;
    width: 100%;
    max-width: 300px;
  }
  </style>