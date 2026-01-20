// React
import { FormEvent, useState } from 'react';
import { Link, useParams } from 'react-router-dom';

// Styles
import '../styles/room.scss';

// Firebase
import { database, ref, set, push, storage } from '../services/firebase';
import { ref as storageRef, uploadBytes, getDownloadURL } from 'firebase/storage';

// Images
import logoImg from '../assets/images/logo.svg';
import iconAI from '../assets/images/ai.png';
import iconSend from '../assets/images/send.png';
import iconAttached from '../assets/images/attached.png';
import robotImg from '../assets/images/robot.png';

// Components
import { RoomCode } from '../components/RoomCode';
import { MessageShare } from '../components/MessageShare';
import { Button } from '../components/Button';
import { Prompt } from '../components/Prompt';

// Hooks
import { useAuth } from '../hooks/useAuth';
import { useRoom } from '../hooks/useRoom';

type PromptType = {
  id: string;
  content: string;
  type: 'Text' | 'PDF' | 'AI' | 'AI_TYPING';
  fileURL?: string;
  author: {
    name: string;
    avatar: string;
  };
};

type RoomParams = {
  id: string;
};

export function Room() {
  const { user, signInWithGoogle } = useAuth();
  const params = useParams<RoomParams>();
  const roomId = String(params.id);

  const { title, prompts } = useRoom(roomId) as {
    title: string;
    prompts: PromptType[];
  };

  const [newQuestion, setNewQuestion] = useState('');
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [selectedFileName, setSelectedFileName] = useState<string | null>(null);
  const [isAIModalOpen, setIsAIModalOpen] = useState(false);
  const [aiTheme, setAiTheme] = useState('');
  const [isIndexing, setIsIndexing] = useState(false);
  const [isAITyping, setIsAITyping] = useState(false);

  async function handleLogin() {
    await signInWithGoogle();
  }

  function handleAttachFile() {
    setIsUploadModalOpen(true);
  }

  function handleCloseModal() {
    setIsUploadModalOpen(false);
    setSelectedFileName(null);
  }

  function handleCloseAIModal() {
    setIsAIModalOpen(false);
    setAiTheme('');
  }

  function handleFileSelection(event: React.ChangeEvent<HTMLInputElement>) {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFileName(file.name);
    } else {
      setSelectedFileName(null);
    }
  }

  // -----------------------------
  // PDF HELPERS
  // -----------------------------
  function openPdfByName(pdfName: string) {
    const pdfPrompt = prompts.find(
      (p) => p.type === 'PDF' && p.content === pdfName
    );

    if (!pdfPrompt || !pdfPrompt.fileURL) {
      alert(`PDF "${pdfName}" not found in this room.`);
      return;
    }

    window.open(pdfPrompt.fileURL, '_blank');
  }

  // -----------------------------
  // AI RESPONSE FORMATTER
  // -----------------------------
  function formatAIResponse(data: any): string {
    if (!data.results || data.results.length === 0) {
      return 'I did not find any relevant documents for this topic.';
    }

    let text = `I found ${data.results.length} relevant document(s):\n\n`;

    data.results.forEach((item: any, index: number) => {
      text += `${index + 1}. 📄 ${item.title}\n`;
      text += `   👤 Researcher: ${item.researcher}\n`;
      text += `   🎯 Score: ${item.score.toFixed(3)}\n`;
      text += `   🧠 Relevant excerpt:\n   "${item.sample_text}"\n\n`;
    });

    return text;
  }

  async function handleSendQuestion(event: FormEvent) {
    event.preventDefault();

    if (newQuestion.trim() === '') return;
    if (!user) throw new Error('You must be logged in');

    const prompt = {
      content: newQuestion,
      type: 'Text',
      author: {
        name: user.name,
        avatar: user.avatar
      }
    };

    const db = database;
    const questionRef = ref(db, `rooms/${roomId}/prompts`);
    const newQuestRef = push(questionRef);
    await set(newQuestRef, prompt);

    setNewQuestion('');
  }


  // -----------------------------
  // AI TYPING PROMPT
  // -----------------------------
  async function pushAITypingMessage() {
    const db = database;
    const promptsRef = ref(db, `rooms/${roomId}/prompts`);

    const typingPrompt = {
      content: '🤖 SummAIze Bot está a escrever...',
      type: 'AI_TYPING',
      author: {
        name: 'SummAIze Bot',
        avatar: robotImg
      }
    };

    const newRef = push(promptsRef);
    await set(newRef, typingPrompt);

    return newRef.key;
  }

  // -----------------------------
  // FILE UPLOAD
  // -----------------------------
  async function handleFileUpload(event: FormEvent) {
    event.preventDefault();

    if (!user) {
      alert('You must be logged in to attach documents.');
      return;
    }

    const input = document.getElementById(
      'pdf-file-upload'
    ) as HTMLInputElement;

    const file = input.files?.[0];

    if (!file) {
      alert('No file selected');
      return;
    }

    if (file.type !== 'application/pdf') {
      alert('Please, select a PDF file');
      return;
    }

    try {
      setIsIndexing(true);

      const fileStorageRef = storageRef(
        storage,
        `rooms/${roomId}/attachments/${file.name}`
      );

      const uploadResult = await uploadBytes(fileStorageRef, file);
      const downloadURL = await getDownloadURL(uploadResult.ref);

      const pdfPrompt = {
        content: file.name,
        type: 'PDF',
        fileURL: downloadURL,
        author: {
          name: user.name,
          avatar: user.avatar
        }
      };

      const db = database;
      const promptsRef = ref(db, `rooms/${roomId}/prompts`);
      const newPromptRef = push(promptsRef);
      await set(newPromptRef, pdfPrompt);

      const response = await fetch(
        'http://127.0.0.1:8000/api/upload_pdf',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            roomId: roomId,
            promptId: newPromptRef.key,
            title: file.name.replace('.pdf', ''),
            researcher: user.name,
            fileURL: downloadURL
          })
        }
      );

      if (!response.ok) {
        const errText = await response.text();
        throw new Error(errText);
      }

      handleCloseModal();
    } catch (error) {
      console.error('Error during upload or AI indexing:', error);
      alert('Upload succeeded, but AI indexing failed. Check console.');
    } finally {
      setIsIndexing(false);
    }
  }

  // -----------------------------
  // AI SEARCH
  // -----------------------------
  async function handleSubmitAIModal(event: FormEvent) {
    event.preventDefault();

    if (aiTheme.trim() === '') return;

    setIsAITyping(true);
    let typingPromptKey: string | null = null;

    try {
      typingPromptKey = await pushAITypingMessage();

      const response = await fetch(
        `http://127.0.0.1:8000/api/search/${roomId}`,
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            query: aiTheme,
            threshold: 0.4
          })
        }
      );

      if (!response.ok) {
        const errText = await response.text();
        throw new Error(errText);
      }

      const data = await response.json();
      const aiMessage = formatAIResponse(data);

      const db = database;
      const aiPromptRef = ref(
        db,
        `rooms/${roomId}/prompts/${typingPromptKey}`
      );

      await set(aiPromptRef, {
        content: aiMessage,
        type: 'AI',
        author: {
          name: 'SummAIze Bot',
          avatar: robotImg
        }
      });
    } catch (error) {
      console.error('Error during AI search:', error);
      alert('AI search failed. Check console.');
    } finally {
      setIsAITyping(false);
      handleCloseAIModal();
    }
  }

  return (
    <div id="page-room">
      <header>
        <div className="content">
          <Link to="/">
            <img src={logoImg} alt="SummAIze" />
          </Link>
          <RoomCode code={roomId} />
        </div>
      </header>

      <main>
        <div className="room-title">
          <h1>Room {title}</h1>
          {prompts.length > 0 && (
            <span>{prompts.length} prompt(s)</span>
          )}
        </div>

        <div className="prompt-list">
          <div className="prompt-container">
            {prompts.map((prompt) => {
              return (
                <Prompt
                  key={prompt.id}
                  content={prompt.content}
                  author={prompt.author}
                  type={prompt.type}
                  fileURL={prompt.fileURL}
                />
              );
            })}
          </div>
        </div>

        {prompts.length < 1 && <MessageShare admin />}

        <form onSubmit={handleSendQuestion}>
          <textarea
            placeholder="Write here..."
            onChange={(event) =>
              setNewQuestion(event.target.value)
            }
            value={newQuestion}
          />

          <div className="form-footer">
            {user ? (
              <div className="user-info">
                <img src={user.avatar} alt={user.name} />
                <span>{user.name}</span>
              </div>
            ) : (
              <span>
                To write,{' '}
                <button
                  onClick={handleLogin}
                  className="btn"
                >
                  you need to Login
                </button>
                .
              </span>
            )}

            <div className="btn-section">
              <Button
                className="btn-icon"
                type="button"
                onClick={handleAttachFile}
                disabled={!user || isIndexing}
              >
                <img className="icon" src={iconAttached} />
              </Button>

              <Button
                className="btn-icon"
                type="button"
                onClick={() => setIsAIModalOpen(true)}
                disabled={!user}
              >
                <img className="icon" src={iconAI} />
              </Button>


              <Button
                className="btn-icon"
                type="submit"
                disabled={!user}
              >
                <img
                  className="icon"
                  src={iconSend}
                  alt="send"
                />
              </Button>
            </div>
          </div>
        </form>
      </main>

      {isUploadModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            {!isIndexing ? (
              <>
                <h2>Attach PDF File</h2>

                <form onSubmit={handleFileUpload}>
                  <label
                    htmlFor="pdf-file-upload"
                    className="file-upload-label"
                  >
                    <span>
                      {selectedFileName || 'Select File'}
                    </span>
                  </label>

                  <input
                    id="pdf-file-upload"
                    type="file"
                    accept=".pdf"
                    style={{ display: 'none' }}
                    onChange={handleFileSelection}
                  />

                  <div className="modal-actions">
                    <Button
                      type="button"
                      onClick={handleCloseModal}
                      disabled={isIndexing}
                    >
                      Cancel
                    </Button>

                    <Button
                      type="submit"
                      disabled={!selectedFileName || isIndexing}
                    >
                      Attach
                    </Button>
                  </div>
                </form>
              </>
            ) : (
              <>
                <h2>Indexing PDF</h2>
                <p>
                  ⏳ Uploading and processing your document...
                  <br />
                  This may take a few seconds.
                </p>
              </>
            )}
          </div>
        </div>
      )}

      {isAIModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>What theme are you searching?</h2>

            <form onSubmit={handleSubmitAIModal}>
              <input
                type="text"
                placeholder="e.g. Climate change, AI in healthcare..."
                value={aiTheme}
                onChange={(e) => setAiTheme(e.target.value)}
                className="text-input"
              />

              <div className="modal-actions">
                <Button
                  type="button"
                  onClick={handleCloseAIModal}
                >
                  Cancel
                </Button>

                <Button type="submit">
                  Submit
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}

    </div>
  );
}
