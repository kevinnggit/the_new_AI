
<template>
  <div id="app-container">
    <div class="main-card">
      <header class="app-header">
        <h1>NSPACE AI</h1>
        <p>Chatte oder lass ein Bild analysieren</p>
        <div class="view-switcher">
          <button @click="activeView = 'chat'" :class="{ active: activeView === 'chat' }">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
            <span>Chat</span>
          </button>
          <button @click="activeView = 'image'" :class="{ active: activeView === 'image' }">
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
            <span>Bilderkennung</span>
          </button>
        </div>
      </header>

      <main class="content-area">
        <!-- Chat-Ansicht -->
        <div v-if="activeView === 'chat'" class="chat-view">
          <div class="chat-window" ref="chatWindow">
            <div v-for="(msg, index) in chatHistory" :key="index" :class="['message', msg.isUser ? 'user-message' : 'ai-message']">
              <p>{{ msg.text }}</p>
            </div>
            <div v-if="isLoading" class="message ai-message loading-indicator">
              <span></span><span></span><span></span>
            </div>
          </div>
          <div class="chat-input-area">
            <input type="text" v-model="userInput" @keyup.enter="sendMessage" placeholder="Stelle eine Frage..." :disabled="isLoading" />
            <button @click="sendMessage" :disabled="isLoading || !userInput">Senden</button>
          </div>
        </div>

        <!-- Bilderkennungs-Ansicht -->
        <div v-if="activeView === 'image'" class="image-view">
          <div class="image-uploader" @click="triggerFileInput" @dragover.prevent @drop.prevent="handleFileDrop">
            <template v-if="!imagePreviewUrl">
              <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"><path d="M21.2 15c.7-1.2 1-2.5.7-3.9-.6-2.4-2.4-4.2-4.8-4.8-.9-.3-1.8-.5-2.7-.5-1.5 0-2.8.6-3.9.7-1.2.1-2.5-.4-3.5-1.1C5.6 4.9 4 5.8 3.3 7.5c-.8 2-.2 4.2 1.2 5.6.8.8 1.8 1.3 2.8 1.5l.3.1c.9.2 1.8.4 2.7.7 1.2.4 2.3 1 3.2 1.8.9.8 1.8 1.8 2.5 2.8.5.8 1.3 1.3 2.1 1.5.8.2 1.7.1 2.5-.3z"></path><path d="M7 21a2 2 0 0 0 2-2v-1a2 2 0 0 0-2-2Z"></path><path d="M19 21a2 2 0 0 1-2-2v-1a2 2 0 0 1 2-2Z"></path></svg>
              <span>Bild hierher ziehen oder klicken</span>
            </template>
            <img v-else :src="imagePreviewUrl" alt="Bildvorschau" class="image-preview" />
            <input type="file" ref="fileInput" @change="handleFileSelect" accept="image/png, image/jpeg" style="display: none;" />
          </div>
          <button @click="analyzeImage" :disabled="!selectedImage || isLoading" class="analyze-button">
            {{ isLoading ? 'Analysiere...' : 'Bild analysieren' }}
          </button>
          <div v-if="imageDescription" class="image-description">
            <h3>KI-Analyse:</h3>
            <p>{{ imageDescription }}</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue';

const activeView = ref('chat');
const chatHistory = ref([
  { text: 'Hallo! Wie kann ich dir heute helfen?', isUser: false }
]);
const userInput = ref('');
const isLoading = ref(false);
const chatWindow = ref(null);

const selectedImage = ref(null);
const imagePreviewUrl = ref('');
const imageDescription = ref('');
const fileInput = ref(null);

const API_URL = 'http://localhost:8000'; // URL zu unserem Backend

// Funktion, um nach unten zu scrollen
const scrollToBottom = () => {
  nextTick(() => {
    if (chatWindow.value) {
      chatWindow.value.scrollTop = chatWindow.value.scrollHeight;
    }
  });
};

// Funktion zum Senden einer Chat-Nachricht
const sendMessage = async () => {
  if (!userInput.value.trim()) return;

  const userMessage = { text: userInput.value, isUser: true };
  chatHistory.value.push(userMessage);
  userInput.value = '';
  isLoading.value = true;
  scrollToBottom();

  try {
    const response = await fetch(`${API_URL}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(chatHistory.value.map(msg => ({
          isUser: msg.isUser,
          text: msg.text
      })))
    });
    if (!response.ok) {
      let detail = 'Netzwerkfehler';
      try {
        const err = await response.json();
        if (err && err.detail) detail = err.detail;
      } catch {}
      throw new Error(detail);
    }

    const data = await response.json();
    chatHistory.value.push({ text: data.reply, isUser: false });
  } catch (error) {
    console.error('Fehler beim Senden der Nachricht:', error);
    let msg = 'Unbekannter Fehler';
    try {
      if (error && error.message) msg = String(error.message);
    } catch {}
    chatHistory.value.push({ text: `Fehler: ${msg}`, isUser: false });
  } finally {
    isLoading.value = false;
    scrollToBottom();
  }
};

// --- Bilderkennungs-Funktionen ---
const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileSelect = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedImage.value = file;
    imagePreviewUrl.value = URL.createObjectURL(file);
    imageDescription.value = ''; // Beschreibung zurücksetzen
  }
};

const handleFileDrop = (event) => {
  const file = event.dataTransfer.files[0];
  if (file && file.type.startsWith('image/')) {
    selectedImage.value = file;
    imagePreviewUrl.value = URL.createObjectURL(file);
    imageDescription.value = ''; // Beschreibung zurücksetzen
  }
};

const analyzeImage = async () => {
  if (!selectedImage.value) return;

  isLoading.value = true;
  imageDescription.value = '';
  const formData = new FormData();
  formData.append('image', selectedImage.value);
  formData.append('prompt', 'Beschreibe dieses Bild für jemanden, der es nicht sehen kann.');

  try {
    const response = await fetch(`${API_URL}/api/recognize-image`, {
      method: 'POST',
      body: formData
    });
    if (!response.ok) {
      let detail = 'Netzwerkfehler';
      try {
        const err = await response.json();
        if (err && err.detail) detail = err.detail;
      } catch {}
      throw new Error(detail);
    }
    const data = await response.json();
    imageDescription.value = data.description;
  } catch (error) {
    console.error('Fehler bei der Bildanalyse:', error);
    let msg = 'Unbekannter Fehler';
    try {
      if (error && error.message) msg = String(error.message);
    } catch {}
    imageDescription.value = `Analyse fehlgeschlagen: ${msg}`;
  } finally {
    isLoading.value = false;
  }
};
</script>

<style>
/* Global Styles & Design */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;700&display=swap');

:root {
  --bg-color: #1a1a2e;
  --card-bg-color: #16213e;
  --primary-color: #0f3460;
  --secondary-color: #e94560;
  --text-color: #e0e0e0;
  --text-muted-color: #a0a0a0;
  --border-color: #2a3a5e;
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Inter', sans-serif;
  background-color: var(--bg-color);
  color: var(--text-color);
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 2rem;
  background-image: url('./background.png');
  background-size: cover;
  background-position: center;
}

#app-container {
  width: 100%;
  max-width: 800px;
  height: 85vh;
  max-height: 800px;
}

.main-card {
  background-color: rgba(22, 33, 62, 0.9);
  backdrop-filter: blur(10px);
  border-radius: 20px;
  border: 1px solid var(--border-color);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  height: 100%;
  overflow: hidden;
}

.app-header {
  padding: 1.5rem 2rem;
  border-bottom: 1px solid var(--border-color);
  text-align: center;
}

.app-header h1 {
  font-size: 1.8rem;
  font-weight: 700;
  color: #fff;
}

.app-header p {
  color: var(--text-muted-color);
  margin-top: 0.25rem;
}

.view-switcher {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 1.5rem;
}

.view-switcher button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--primary-color);
  border: 1px solid var(--border-color);
  color: var(--text-color);
  padding: 0.75rem 1.5rem;
  border-radius: 50px;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.3s ease;
}

.view-switcher button:hover {
  background-color: #1a4a8a;
  border-color: #4a6fa5;
}

.view-switcher button.active {
  background: var(--secondary-color);
  color: #fff;
  border-color: var(--secondary-color);
  box-shadow: 0 0 15px rgba(233, 69, 96, 0.4);
}

.content-area {
  flex-grow: 1;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* Chat View */
.chat-view {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.chat-window {
  flex-grow: 1;
  overflow-y: auto;
  padding: 0 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}
/* Custom Scrollbar */
.chat-window::-webkit-scrollbar { width: 6px; }
.chat-window::-webkit-scrollbar-track { background: transparent; }
.chat-window::-webkit-scrollbar-thumb { background: var(--primary-color); border-radius: 3px; }
.chat-window::-webkit-scrollbar-thumb:hover { background: #1a4a8a; }

.message {
  max-width: 75%;
  padding: 0.75rem 1.25rem;
  border-radius: 18px;
  line-height: 1.5;
  word-wrap: break-word;
}

.user-message {
  background-color: var(--secondary-color);
  color: #fff;
  align-self: flex-end;
  border-bottom-right-radius: 4px;
}

.ai-message {
  background-color: var(--primary-color);
  color: var(--text-color);
  align-self: flex-start;
  border-bottom-left-radius: 4px;
}

.chat-input-area {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  border-top: 1px solid var(--border-color);
}

.chat-input-area input {
  flex-grow: 1;
  background: var(--primary-color);
  border: 1px solid var(--border-color);
  border-radius: 50px;
  padding: 0.75rem 1.25rem;
  color: var(--text-color);
  font-size: 1rem;
}
.chat-input-area input:focus {
  outline: none;
  border-color: var(--secondary-color);
}
.chat-input-area button {
  background: var(--secondary-color);
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  color: #fff;
  cursor: pointer;
  font-weight: 500;
  transition: transform 0.2s ease;
}
.chat-input-area button:hover { transform: scale(1.1); }
.chat-input-area button:disabled { background: #555; cursor: not-allowed; }

/* Loading Indicator */
.loading-indicator span {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--text-color);
  margin: 0 2px;
  animation: bounce 1.4s infinite ease-in-out both;
}
.loading-indicator span:nth-child(1) { animation-delay: -0.32s; }
.loading-indicator span:nth-child(2) { animation-delay: -0.16s; }
@keyframes bounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1.0); } }

/* Image View */
.image-view {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
  padding: 1rem;
  height: 100%;
  overflow-y: auto;
}

.image-uploader {
  width: 100%;
  height: 200px;
  border: 2px dashed var(--border-color);
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--text-muted-color);
}
.image-uploader:hover {
  border-color: var(--secondary-color);
  background-color: var(--primary-color);
}
.image-uploader svg {
  margin-bottom: 1rem;
}

.image-preview {
  width: 100%;
  height: 100%;
  object-fit: contain;
  border-radius: 10px;
}

.analyze-button {
  background: var(--secondary-color);
  color: #fff;
  border: none;
  padding: 0.75rem 2rem;
  border-radius: 50px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}
.analyze-button:disabled {
  background: #555; cursor: not-allowed;
}
.analyze-button:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(233, 69, 96, 0.3);
}

.image-description {
  width: 100%;
  background: var(--primary-color);
  border-radius: 12px;
  padding: 1.5rem;
  border: 1px solid var(--border-color);
}
.image-description h3 {
  margin-bottom: 0.75rem;
  color: var(--secondary-color);
}
.image-description p {
  line-height: 1.6;
}
:root {
  --bg-color: #1a1a2e;
  --card-bg-color: #16213e;
  --primary-color: #0f3460;
  --secondary-color: #e94560;
  --text-color: #e0e0e0;
  --text-muted-color: #a0a0a0;
  --border-color: #2a3a5e;
}

</style>
