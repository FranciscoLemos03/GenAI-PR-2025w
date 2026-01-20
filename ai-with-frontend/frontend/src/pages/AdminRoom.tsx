// React Imports
import { FormEvent, useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';

// Firebase
import {
  database,
  ref,
  remove,
  update,
  push,
  set,
  storage
} from '../services/firebase';

import {
  ref as storageRef,
  uploadBytes,
  getDownloadURL,
  deleteObject
} from 'firebase/storage';

// Images
import logoImg from '../assets/images/logo.svg';
import deleteImg from '../assets/images/delete.svg';
import iconAI from '../assets/images/ai.png';
import iconSend from '../assets/images/send.png';
import iconAttached from '../assets/images/attached.png';
import robotImg from '../assets/images/robot.png';

// Components
import { Button } from '../components/Button';
import { RoomCode } from '../components/RoomCode';
import { Prompt } from '../components/Prompt';
import { MessageShare } from '../components/MessageShare';
import { Popup } from '../components/Popup';

// Hooks
import { useRoom } from '../hooks/useRoom';
import { useAuth } from '../hooks/useAuth';

// Styles
import '../styles/room.scss';

type RoomParams = {
  id: string;
};

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

export function AdminRoom() {
  const { user, signInWithGoogle } = useAuth();
  const params = useParams<RoomParams>();
  const roomId = String(params.id);
  const navigate = useNavigate();

  const { title, prompts } = useRoom(roomId) as {
    title: string;
    prompts: PromptType[];
  };

  const [newPrompt, setNewPrompt] = useState('');
  const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
  const [selectedFileName, setSelectedFileName] =
    useState<string | null>(null);
  const [isAIModalOpen, setIsAIModalOpen] = useState(false);
  const [aiTheme, setAiTheme] = useState('');
  const [isIndexing, setIsIndexing] = useState(false);
  const [showPopup, setShowPopup] = useState(false);
  const [promptIdToDelete, setPromptIdToDelete] =
    useState<string | null>(null);
  const [showEndPopup, setShowEndPopup] = useState(false);

  // -----------------------------
  // AUTH
  // -----------------------------
  async function handleLogin() {
    await signInWithGoogle();
  }

  // -----------------------------
  // ROOM CONTROL
  // -----------------------------
  function handleOpenEndPopup() {
    setShowEndPopup(true);
  }

  function handleCloseEndPopup() {
    setShowEndPopup(false);
  }

  async function handleEndRoom() {
    const db = database;
    const roomRef = ref(db, `rooms/${roomId}`);

    await update(roomRef, {
      endedAt: new Date()
    });

    setShowEndPopup(false);
    navigate('/');
  }

  // -----------------------------
  // DELETE PROMPT
  // -----------------------------
  function handleOpenPopup(promptId: string) {
    setPromptIdToDelete(promptId);
    setShowPopup(true);
  }

  function handleClosePopup() {
    setShowPopup(false);
    setPromptIdToDelete(null);
  }

  async function handleDeletePrompt() {
    const promptId = promptIdToDelete;
    if (!promptId) return;

    const promptToDelete = prompts.find(
      (p) => p.id === promptId
    );

    try {
      if (promptToDelete) {
        // Delete PDF from storage if needed
        if (
          promptToDelete.type === 'PDF' &&
          promptToDelete.fileURL
        ) {
          const filename = promptToDelete.content;
          const fileRef = storageRef(
            storage,
            `rooms/${roomId}/attachments/${filename}`
          );
          await deleteObject(fileRef);
        }

        // Delete from database
        const db = database;
        const promptRef = ref(
          db,
          `rooms/${roomId}/prompts/${promptId}`
        );
        await remove(promptRef);
      }
    } catch (error) {
      console.error('Error deleting prompt:', error);
      alert('Error deleting prompt. Check console.');
    }

    handleClosePopup();
  }

  // -----------------------------
  // MODALS
  // -----------------------------
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

  function handleFileSelection(
    event: React.ChangeEvent<HTMLInputElement>
  ) {
    const file = event.target.files?.[0];
    setSelectedFileName(file ? file.name : null);
  }

  // -----------------------------
  // AI HELPERS
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
  // FILE UPLOAD + AI INDEXING
  // -----------------------------
  async function handleFileUpload(event: FormEvent) {
    event.preventDefault();
    if (!user) return;

    const input = document.getElementById(
      'pdf-file-upload'
    ) as HTMLInputElement;

    const file = input.files?.[0];
    if (!file || file.type !== 'application/pdf') {
      alert('Please select a valid PDF file.');
      return;
    }

    try {
      setIsIndexing(true);

      // Upload to Firebase Storage
      const fileStorageRef = storageRef(
        storage,
        `rooms/${roomId}/attachments/${file.name}`
      );

      const uploadResult = await uploadBytes(
        fileStorageRef,
        file
      );

      const downloadURL = await getDownloadURL(
        uploadResult.ref
      );

      // Save PDF prompt
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

      // Call backend AI indexer
      const response = await fetch(
        'http://127.0.0.1:8000/api/upload_pdf',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            roomId,
            promptId: newPromptRef.key,
            title: file.name.replace('.pdf', ''),
            researcher: user.name,
            fileURL: downloadURL
          })
        }
      );

      if (!response.ok) {
        throw new Error(await response.text());
      }

      console.log(
        'GenAI indexed PDF:',
        await response.json()
      );

      handleCloseModal();
    } catch (error) {
      console.error('Upload or indexing failed:', error);
      alert('Upload succeeded, but AI indexing failed.');
    } finally {
      setIsIndexing(false);
    }
  }

  // -----------------------------
  // AI SEARCH
  // -----------------------------
  async function handleSubmitAIModal(
    event: FormEvent
  ) {
    event.preventDefault();
    if (!aiTheme.trim()) return;

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
        throw new Error(await response.text());
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
      console.error('AI search failed:', error);
      alert('AI search failed. Check console.');
    } finally {
      handleCloseAIModal();
    }
  }

  // -----------------------------
  // TEXT PROMPT
  // -----------------------------
  async function handleSendPrompt(
    event: FormEvent
  ) {
    event.preventDefault();
    if (!newPrompt.trim() || !user) return;

    const prompt = {
      content: newPrompt,
      type: 'Text',
      author: {
        name: user.name,
        avatar: user.avatar
      }
    };

    const db = database;
    const promptRef = ref(
      db,
      `rooms/${roomId}/prompts`
    );

    const newQuestRef = push(promptRef);
    await set(newQuestRef, prompt);

    setNewPrompt('');
  }

  // -----------------------------
  // RENDER
  // -----------------------------
  return (
    <div id="page-room">
      <header>
        <div className="content">
          <Link to="/">
            <img src={logoImg} alt="SummAIze" />
          </Link>

          <div>
            <RoomCode code={roomId} />
            <Button isOutlined onClick={handleOpenEndPopup}>
              End Room
            </Button>
          </div>
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
            {prompts.map((prompt) => (
              <Prompt
                key={prompt.id}
                content={prompt.content}
                author={prompt.author}
                type={prompt.type}
                fileURL={prompt.fileURL}
              >
                <button
                  type="button"
                  onClick={() =>
                    handleOpenPopup(prompt.id)
                  }
                >
                  <img
                    src={deleteImg}
                    alt="Delete"
                  />
                </button>
              </Prompt>
            ))}
          </div>
        </div>

        {prompts.length < 1 && <MessageShare admin />}

        <form onSubmit={handleSendPrompt}>
          <textarea
            placeholder="Write here..."
            onChange={(e) =>
              setNewPrompt(e.target.value)
            }
            value={newPrompt}
          />

          <div className="form-footer">
            {user ? (
              <div className="user-info">
                <img
                  src={user.avatar}
                  alt={user.name}
                />
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
                <img
                  className="icon"
                  src={iconAttached}
                  alt="Attach"
                />
              </Button>

              <Button
                className="btn-icon"
                type="button"
                onClick={() =>
                  setIsAIModalOpen(true)
                }
                disabled={!user}
              >
                <img
                  className="icon"
                  src={iconAI}
                  alt="AI"
                />
              </Button>

              <Button
                className="btn-icon"
                type="submit"
                disabled={!user}
              >
                <img
                  className="icon"
                  src={iconSend}
                  alt="Send"
                />
              </Button>
            </div>
          </div>
        </form>
      </main>

      {/* Upload Modal */}
      {isUploadModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            {!isIndexing ? (
              <>
                <h2>Attach PDF</h2>

                <form onSubmit={handleFileUpload}>
                  <label
                    htmlFor="pdf-file-upload"
                    className="file-upload-label"
                  >
                    <span>
                      {selectedFileName ||
                        'Select File'}
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
                    >
                      Cancel
                    </Button>

                    <Button
                      type="submit"
                      disabled={
                        !selectedFileName ||
                        isIndexing
                      }
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
                  ⏳ Uploading and processing your
                  document...
                  <br />
                  This may take a few seconds.
                </p>
              </>
            )}
          </div>
        </div>
      )}

      {/* AI Modal */}
      {isAIModalOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <h2>What theme are you searching?</h2>

            <form onSubmit={handleSubmitAIModal}>
              <input
                type="text"
                placeholder="e.g. GPT LLM, AI in healthcare..."
                value={aiTheme}
                onChange={(e) =>
                  setAiTheme(e.target.value)
                }
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

      {/* Delete Popup */}
      {showPopup && (
        <Popup
          prompt
          functionCancel={handleClosePopup}
          functionConfirm={handleDeletePrompt}
        />
      )}

      {/* End Room Popup */}
      {showEndPopup && (
        <Popup
          functionCancel={handleCloseEndPopup}
          functionConfirm={handleEndRoom}
        />
      )}
    </div>
  );
}
