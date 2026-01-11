// React Imports
import { FormEvent, useEffect, useState } from 'react';
import { Link, useNavigate, useParams} from 'react-router-dom';

// Firebase
import { database, ref, remove, update, push, set, storage} from '../services/firebase';
import { ref as storageRef, uploadBytes, getDownloadURL, deleteObject } from 'firebase/storage';

// Image Imports
import logoImg from '../assets/images/logo.svg';
import deleteImg from '../assets/images/delete.svg';
import iconAI from '../assets/images/ai.png';
import iconSend from '../assets/images/send.png';
import iconAttached from '../assets/images/attached.png';

//Components Imports
import { Button } from '../components/Button';
import { RoomCode } from '../components/RoomCode';
import { Prompt } from '../components/Prompt';
import { MessageShare } from '../components/MessageShare';
import { Popup } from '../components/Popup';

import '../styles/room.scss';
import { useRoom } from '../hooks/useRoom';
import { useAuth } from '../hooks/useAuth';

type RoomParams = {
    id: string;
}

type PromptType = {
    id: string;
    content: string;
    type: 'Text' | 'PDF';
    fileURL?: string; 
    author: {
        name: string;
        avatar: string;
    };
}


export function AdminRoom() {

    const {user, signInWithGoogle} = useAuth();
    const params = useParams<RoomParams>(); 
    const roomId = String(params.id);
    const navigate = useNavigate();

    const [newPrompt, setNewPrompt] = useState('');
    const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
    const [selectedFileName, setSelectedFileName] = useState<string | null>(null);
    const [isAIModalOpen, setIsAIModalOpen] = useState(false);
    const [aiTheme, setAiTheme] = useState('');
    const [ showPopup, setShowPopup ] = useState(false)
    const [ promptIdToDelete, setPromptIdToDelete ] = useState<string | null>(null);
    const [ showEndPopup, setShowEndPopup ] = useState(false)
    const {title, prompts} = useRoom(roomId) as { title: string; prompts: PromptType[] };

    function handleOpenPopup(promptId: string){
        setPromptIdToDelete(promptId);
        setShowPopup(true)
    }
    function handleClosePopup(){
        setShowPopup(false)
        setPromptIdToDelete(null);
    }
    function handleOpenEndPopup(){
        setShowEndPopup(true)
    }
    function handleCloseEndPopup(){
        setShowEndPopup(false)
    }
    
    async function handleEndRoom() {
        const db = database;
        const roomRef = ref(db, `rooms/${roomId}`)
        await update(roomRef, {
            endedAt: new Date(),
        })

        setShowEndPopup(false)
        
        navigate('/')
    }

    async function handleDeletePrompt(){
        
        const promptId = promptIdToDelete;

        if (!promptId) {
            alert('Error: Prompt ID not found');
            handleClosePopup();
            return;
        }

        // 1. Search the current list for the prompt to obtain the type and fileURL
        const promptToDelete = prompts.find(p => p.id === promptId);
        
        // Delete Logic
        try {
            if (promptToDelete) {
                // 2. CONDITIONAL VERIFICATION AND DELETION OF STORAGE
                if (promptToDelete.type === 'PDF' && promptToDelete.fileURL) {

                    const filename = promptToDelete.content;
                    
                    if (filename) {
                        const fileToDeleteRef = storageRef(storage, `rooms/${roomId}/attachments/${filename}`);
                        await deleteObject(fileToDeleteRef);
                    }
                }

                // 3. DELETE FROM REALTIME DATABASE
                const db = database;
                const promptRef = ref(db, `rooms/${roomId}/prompts/${promptId}`);
                await remove(promptRef);
            } else {
                alert('Error: Prompt not found in the list');
            }
        } catch (error) {
            console.error('Error deleting the prompt', error);
            
            alert('Error: Watch the console');
        }

        handleClosePopup();
    }
    
    // --- Funções do Room.tsx (Integradas) ---

    async function handleLogin(){
        await signInWithGoogle()
    }

    function handleAttachFile() {
        setIsUploadModalOpen(true);
    }

    function handleCloseAIModal() {
        setIsAIModalOpen(false);
        setAiTheme('');
    }

    function handleSubmitAIModal(event: FormEvent) {
        event.preventDefault();

        if (aiTheme.trim() === '') {
            return;
        }

        // 🚧 Aqui depois ligas à lógica de AI
        console.log('AI Theme:', aiTheme);

        handleCloseAIModal();
    }

    
    function handleCloseModal() {
        setIsUploadModalOpen(false);
        setSelectedFileName(null);
    }

    function handleFileSelection(event: React.ChangeEvent<HTMLInputElement>) {
        const file = event.target.files?.[0];
        
        if (file) {
            setSelectedFileName(file.name);
        } else {
            setSelectedFileName(null);
        }
    }

    async function handleFileUpload(event: FormEvent) {
        event.preventDefault();
        
        if (!user) {
            alert('You need to be logged in');
            return;
        }

        const input = document.getElementById('pdf-file-upload') as HTMLInputElement;
        const file = input.files?.[0];

        if (!file) {
            alert('No file selected');
            return;
        }
        
        if (file.type !== 'application/pdf') {
            alert('Please select a PDF file.');
            return;
        }
        
        try {
            // 1. Create the reference on Firebase Storage
            const fileStorageRef = storageRef(storage, `rooms/${roomId}/attachments/${file.name}`);
            
            // 2. Upload PDF File
            const uploadResult = await uploadBytes(fileStorageRef, file);

            // 3. Get the Public Download URL
            const downloadURL = await getDownloadURL(uploadResult.ref);
            
            // 4. Create the Prompt Object (with PDF type) for the Realtime Database
            const pdfPrompt = {
                content: file.name,
                type: "PDF",
                fileURL: downloadURL,
                author: {
                    name: user.name,
                    avatar: user.avatar
                },
            };

            // 5. Save metadata on Realtime Database
            const db = database;
            const promptsRef = ref(db, `rooms/${roomId}/prompts`);
            const newPromptRef = push(promptsRef);
            await set(newPromptRef, pdfPrompt);

        } catch (error) {
            console.error('Error during the upload:', error);
            alert('Error - Watch console');
        } finally {
            handleCloseModal();
        }
    }

    function handleAIGenerate() {
        
        setIsAIModalOpen(true);

    }

    // Text Submission
    async function handleSendPrompt(event: FormEvent){
        event.preventDefault();
    
        if (newPrompt.trim() === ''){
            return
        }
        if (!user) {
            throw new Error('You must be logged in')
        }

        const prompt = {
            content: newPrompt,
            type: "Text",
            author: {
                name: user.name,
                avatar: user.avatar
            },
        };

        const db = database;
        const promptRef = ref(db, `rooms/${roomId}/prompts`);
        const newQuestRef = push(promptRef);
        await set (newQuestRef, prompt)

        setNewPrompt('');
    }

    return(
        <div id="page-room">
            <header>
                <div className="content">
                    <Link to="/"><img src={logoImg} alt="SummAIze" /></Link>
                    
                    <div >
                        <RoomCode code={roomId} />
                        <Button isOutlined onClick={handleOpenEndPopup}>End Room</Button>
                    </div>
                </div>
            </header>

            <main>
                <div className="room-title">
                    <h1>Room {title}</h1>
                    {
                        prompts.length > 0 &&  <span>{prompts.length} prompts(s)</span>
                    }
                </div>
                
                <div className="prompt-list">
                    <div className="prompt-container">
                        {   
                            prompts.map(prompt => {
                                return(
                                    <Prompt 
                                        key={prompt.id}
                                        content={prompt.content}
                                        author={prompt.author}
                                        type={prompt.type}
                                        fileURL={prompt.fileURL}
                                    >
                                        <button
                                            type='button'
                                            onClick={() => handleOpenPopup(prompt.id)}
                                        >
                                            <img src={deleteImg} alt="Delete" />
                                        </button>
                                    </Prompt>
                                )
                            })
                        }
                    </div>
                </div>
                
                { prompts.length < 1 && (<MessageShare admin/>) }
                
                <form onSubmit={handleSendPrompt}>
                    <textarea 
                        placeholder='Write here...'
                        onChange={(event) => {setNewPrompt(event.target.value);}}
                        value={newPrompt}
                    />

                    <div className="form-footer">
                        {
                            user ? (
                                <div className="user-info">
                                    <img src={user.avatar} alt={user.name} />
                                    <span>{user.name}</span>
                                </div>
                            ) : (
                                <span>To write, <button onClick={handleLogin} className="btn">you need to Login</button>.</span>
                                )
                        }
                        <div className="btn-section">
                            <Button className="btn-icon" type="button" onClick={handleAttachFile} disabled={!user}><img className='icon' src={iconAttached} alt="Attach file"/></Button>
                            <Button className="btn-icon" type="button" onClick={handleAIGenerate} disabled={!user}><img className='icon' src={iconAI} alt="AI"/></Button>
                            <Button className="btn-icon" type="submit" disabled={!user}><img className='icon' src={iconSend} alt={"Submit"} /></Button>
                        </div>
                    </div>
                </form>

            </main>

            {isUploadModalOpen && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h2>Attach PDF</h2>
                        
                        <form onSubmit={handleFileUpload}>
                            <label htmlFor="pdf-file-upload" className="file-upload-label">
                                <span>{selectedFileName || 'Select File'}</span>
                            </label>
                            
                            <input 
                                id="pdf-file-upload" 
                                type="file" 
                                accept=".pdf" 
                                style={{ display: 'none' }}
                                onChange={handleFileSelection}
                            />
                            
                            <div className="modal-actions">
                                <Button type="button" onClick={handleCloseModal} >
                                    Cancel
                                </Button>
                                <Button type="submit">
                                    Attach
                                </Button>
                            </div>
                        </form>
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
                                placeholder="Ex:. GPT LLM, AI in healthcare..."
                                value={aiTheme}
                                onChange={(e) => setAiTheme(e.target.value)}
                                className="text-input"
                            />

                            <div className="modal-actions">
                                <Button type="button" onClick={handleCloseAIModal}>
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


            {   
                showPopup && (
                    <Popup 
                        prompt 
                        functionCancel={handleClosePopup}
                        functionConfirm={handleDeletePrompt}
                    />
                )
            }

            {   
                showEndPopup && (
                    <Popup 
                        functionCancel={handleCloseEndPopup}
                        functionConfirm={handleEndRoom} 
                    />
                )
            }

        </div>
    )
}