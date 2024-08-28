// App.js

import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [audioUrl, setAudioUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (text.trim() === '') return;
    
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/speak', { text }, {
        responseType: 'blob', // Expecting a binary response
      });
      const audioBlob = new Blob([response.data], { type: 'audio/wav' });
      const audioUrl = URL.createObjectURL(audioBlob);
      setAudioUrl(audioUrl);
    } catch (error) {
      console.error('Error generating audio:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <div className="header">
        Wygeneruj audio z tekstu, który wprowadzisz!
      </div>
      <div className="content">
        <div className="text-box">
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Wprowadź tu tekst..."
          />
        </div>
        <button className="send-button" onClick={handleSend}>
          Generuj
        </button>
        <div className="audio-container">
          {loading ? (
            <div className="spinner"></div>
          ) : (
            audioUrl && <audio className="audio-player" controls src={audioUrl} />
          )}
        </div>
      </div>
      <footer className="footer">
        Wykonane przez Wiktora Krasińskiego i Przemysława Roślenia<br/> praca magisterska 2024
      </footer>
    </div>
  );
}

export default App;
