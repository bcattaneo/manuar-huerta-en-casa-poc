<!-- ChatScreen.vue -->
<template>
    <div class="chat-container">
      <!-- Barra superior con botón de volver -->
      <div class="chat-header">
        <v-btn
          variant="text"
          density="comfortable"
          icon="mdi-chevron-left"
          color="#6B8E23"
          @click="goBack"
        >
        </v-btn>
        <span v-if="plantContext" class="plant-context">{{ plantContext }}</span>
        <span v-else class="chat-title">Preguntas</span>
      </div>
  
      <!-- Área de mensajes del chat -->
      <div class="chat-messages" ref="messagesContainer">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="['message-container', message.isUser ? 'user-message' : '']"
        >
          <!-- Mensajes del usuario (verde, a la derecha) -->
          <div
            v-if="message.isUser"
            class="message user-bubble"
          >
            {{ message.text }}
          </div>
  
          <!-- Mensajes del sistema (blanco, a la izquierda) -->
          <div
            v-else
            class="message system-bubble"
          >
            <div v-if="message.image" class="message-image-container">
              <img :src="message.image" alt="Ilustración" class="message-image" />
              <v-btn
                v-if="message.hasAudio"
                icon
                variant="text"
                density="comfortable"
                color="grey-darken-1"
                class="audio-button"
              >
                <v-icon>mdi-volume-high</v-icon>
              </v-btn>
            </div>
            <div v-html="formatMessage(message.text)"></div>
          </div>
        </div>
      </div>
  
      <!-- Área de entrada de mensaje -->
      <div class="chat-input">
        <v-text-field
          v-model="newMessage"
          placeholder="Escribe otra pregunta..."
          variant="outlined"
          density="comfortable"
          bg-color="white"
          hide-details
          rounded
          class="message-input"
          @keyup.enter="sendMessage"
        ></v-text-field>
        <v-btn
          icon
          color="#6B8E23"
          class="send-button"
          @click="sendMessage"
        >
          <v-icon>{{ newMessage.trim() ? 'mdi-send' : 'mdi-microphone' }}</v-icon>
        </v-btn>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ChatScreen',
    props: {
      plantContext: {
        type: String,
        default: null
      }
    },
    data() {
      return {
        newMessage: '',
        messages: [],
        mockResponses: {
          general: [
            {
              question: "¿Cómo puedo empezar mi huerta?",
              answer: "Para empezar tu huerta necesitas: un espacio con buena luz, recipientes o tierra preparada, semillas o plantines, y herramientas básicas como pala y regadera. ¡Empieza con plantas fáciles como albahaca o lechuga!",
            },
            {
              question: "¿Cuándo debo regar mi planta?",
              answer: "Para cuidar bien tu planta, hay que regarla en el momento correcto. Aquí tienes algunos consejos fáciles:<br><br>🌱 <b>Revisa la tierra:</b> Antes de echarle agua, toca la tierra con tu dedo. Si está seca hasta unos 2 o 3 cm de profundidad, es momento de regar.<br><br>⏰ <b>Mejor horario:</b> Riega temprano en la mañana o al atardecer, evita las horas de más calor.<br><br>💧 <b>Cantidad justa:</b> El agua debe ser suficiente para humedecer toda la tierra, pero sin que quede encharcada.",
              image: "/src/assets/illustrations/watering.png",
              hasAudio: true
            },
            {
              question: "¿Qué plantas son buenas para principiantes?",
              answer: "Las mejores plantas para principiantes son albahaca, tomate cherry, lechuga, cebollín y zanahoria. Son resistentes y fáciles de cuidar.",
            }
          ],
          plantas: {
            "Tomate": [
              {
                question: "¿Cómo cuido mis tomates?",
                answer: "Los tomates necesitan 6-8 horas de sol dirario, riego regular sin mojar las hojas, y soporte a medida que crecen. Fertiliza cada 2-3 semanas.",
              },
              {
                question: "¿Cuándo cosechar los tomates?",
                answer: "Los tomates están listos para cosechar cuando tienen un color uniforme y ceden ligeramente a la presión. Generalmente 60-85 días después de plantar.",
              }
            ],
            "Pepino": [
              {
                question: "¿Cuánta agua necesitan los pepinos?",
                answer: "Los pepinos necesitan riego constante y generoso. La tierra debe mantenerse húmeda pero no encharcada. En épocas calurosas, pueden necesitar agua diariamente.",
              }
            ],
            "Albahaca": [
              {
                question: "¿Cómo cosechar albahaca sin dañar la planta?",
                answer: "Para cosechar albahaca correctamente, corta justo encima de un par de hojas usando tijeras limpias. Esto estimulará que la planta crezca más frondosa. Nunca arranques las hojas, pues dañarías el tallo.",
              }
            ]
          }
        }
      };
    },
    mounted() {
      // Si hay contexto de planta, mostrar un mensaje inicial
      if (this.plantContext) {
        this.messages.push({
          isUser: false,
          text: `¡Hola! Estoy aquí para responder tus dudas sobre ${this.plantContext}. ¿Qué te gustaría saber?`,
        });
      } else {
        // Mensaje de bienvenida general
        this.messages.push({
          isUser: false,
          text: "¡Hola! Soy tu asistente de huerta. ¿Qué te gustaría saber sobre el cultivo de plantas?",
        });
      }
    },
    methods: {
      goBack() {
        this.$router.go(-1);
      },
      sendMessage() {
        if (!this.newMessage.trim()) return;
        
        // Agregar mensaje del usuario
        this.messages.push({
          isUser: true,
          text: this.newMessage
        });
        
        const userQuestion = this.newMessage;
        this.newMessage = ''; // Limpiar campo de entrada
        
        // Simular tiempo de respuesta
        setTimeout(() => {
          this.receiveResponse(userQuestion);
        }, 1000);
      },
      receiveResponse(question) {
        // Buscar respuesta en el mock según contexto
        let response;
        
        if (this.plantContext) {
          // Buscar en respuestas específicas de la planta
          const plantResponses = this.mockResponses.plantas[this.plantContext];
          if (plantResponses) {
            response = this.findSimilarResponse(question, plantResponses);
          }
        }
        
        // Si no hay respuesta específica, buscar en respuestas generales
        if (!response) {
          response = this.findSimilarResponse(question, this.mockResponses.general);
        }
        
        // Si aún no hay respuesta, dar una genérica
        if (!response) {
          response = {
            answer: "Interesante pregunta. Estoy aprendiendo sobre ese tema. Mientras tanto, ¿te puedo ayudar con información sobre riego, luz solar o nutrientes que necesitan las plantas?",
          };
        }
        
        // Agregar respuesta del sistema
        this.messages.push({
          isUser: false,
          text: response.answer,
          image: response.image || null,
          hasAudio: response.hasAudio || false
        });
        
        // Scroll al último mensaje
        this.$nextTick(() => {
          this.scrollToBottom();
        });
      },
      findSimilarResponse(question, responseList) {
        // Versión simple: compara palabras clave
        // En una app real, usarías NLP o un servicio de IA
        const lowerQuestion = question.toLowerCase();
        
        for (const item of responseList) {
          const keywords = item.question.toLowerCase().split(' ');
          
          // Si la pregunta contiene palabras clave similares
          const hasMatch = keywords.some(word => 
            word.length > 3 && lowerQuestion.includes(word)
          );
          
          if (hasMatch) return item;
        }
        
        // Si no hay coincidencia, devolver el primero (para demostración)
        return responseList[0];
      },
      formatMessage(text) {
        // Aquí podrías añadir formato al texto, como convertir URLs, etc.
        return text;
      },
      scrollToBottom() {
        if (this.$refs.messagesContainer) {
          this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight;
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .chat-container {
    display: flex;
    flex-direction: column;
    height: 100vh;
    max-width: 600px;
    margin: 0 auto;
    background-color: #F3F3F3;
  }
  
  .chat-header {
    display: flex;
    align-items: center;
    padding: 10px 16px;
    background-color: white;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    position: sticky;
    top: 0;
    z-index: 10;
  }
  
  .plant-context, .chat-title {
    margin-left: 10px;
    font-size: 18px;
    font-weight: 500;
    color: #333;
  }
  
  .chat-messages {
    flex: 1;
    overflow-y: auto;
    padding: 16px;
    display: flex;
    flex-direction: column;
    gap: 16px;
  }
  
  .message-container {
    display: flex;
    width: 100%;
  }
  
  .message {
    max-width: 80%;
    padding: 12px 16px;
    border-radius: 18px;
    font-size: 16px;
    line-height: 1.4;
  }
  
  .user-message {
    justify-content: flex-end;
  }
  
  .user-bubble {
    background-color: #C5E1A5; /* Verde claro */
    color: #333;
    border-top-right-radius: 4px;
    text-align: right;
    align-self: flex-end;
  }
  
  .system-bubble {
    background-color: white;
    color: #333;
    border-top-left-radius: 4px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
  }
  
  .message-image-container {
    position: relative;
    margin-bottom: 12px;
  }
  
  .message-image {
    width: 100%;
    border-radius: 12px;
    margin-bottom: 8px;
  }
  
  .audio-button {
    position: absolute;
    top: 10px;
    right: 10px;
    background-color: rgba(255, 255, 255, 0.8);
    border-radius: 50%;
  }
  
  .chat-input {
    display: flex;
    align-items: center;
    padding: 12px 16px;
    background-color: #F3F3F3;
    border-top: 1px solid #E0E0E0;
    position: sticky;
    bottom: 0;
  }
  
  .message-input {
    flex: 1;
  }
  
  .send-button {
    margin-left: 8px;
  }
  </style>