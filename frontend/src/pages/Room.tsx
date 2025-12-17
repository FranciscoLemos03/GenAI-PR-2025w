// React
import { FormEvent, useEffect, useState } from 'react';
import { Link, useParams} from 'react-router-dom';

// Styles
import '../styles/room.scss';

// Firebase
import { database, ref, set, push, remove, storage} from '../services/firebase';
import { ref as storageRef, uploadBytes, getDownloadURL } from 'firebase/storage';

// Images
import logoImg from '../assets/images/logo.svg';
import iconAI from '../assets/images/ai.png';
import iconSend from '../assets/images/send.png';
import iconAttached from '../assets/images/attached.png';

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
    type: 'Text' | 'PDF';
    fileURL?: string; 
    author: {
        name: string;
        avatar: string;
    };
}

export function Room(){

    const {user, signInWithGoogle} = useAuth();
    const params = useParams<RoomParams>();
    const [newQuestion, setNewQuestion] = useState('');
    const roomId = String(params.id);
    const {title, prompts} = useRoom(roomId) as { title: string; prompts: PromptType[] };
    const [isUploadModalOpen, setIsUploadModalOpen] = useState(false);
    const [selectedFileName, setSelectedFileName] = useState<string | null>(null);

    type RoomParams = {
        id: string,
    }    

    async function handleLogin(){
        await signInWithGoogle()
    }

    function handleAttachFile() {
        setIsUploadModalOpen(true);
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
            alert('You must be logged in to attach documents.');
            return;
        }

        const input = document.getElementById('pdf-file-upload') as HTMLInputElement;
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
            const fileStorageRef = storageRef(storage, `rooms/${roomId}/attachments/${file.name}`);
            
            const uploadResult = await uploadBytes(fileStorageRef, file);

            const downloadURL = await getDownloadURL(uploadResult.ref);
            
            const pdfPrompt = {
                content: file.name,
                type: "PDF",
                fileURL: downloadURL,
                author: {
                    name: user.name,
                    avatar: user.avatar
                },
            };

            const db = database;
            const promptsRef = ref(db, `rooms/${roomId}/prompts`);
            const newPromptRef = push(promptsRef);
            await set(newPromptRef, pdfPrompt);

        } catch (error) {
            console.error('Error during upload or saving to the database:', error);
            alert('Error - Please check the console.');
        } finally {
            handleCloseModal();
        }
    }

    function handleAIGenerate() {
                
        ///                \\\
        //                  \\
        //      To Do       \\
        //                  \\
        ///                \\\

    }

    async function handleSendQuestion(event: FormEvent){
        event.preventDefault();
    
        if (newQuestion.trim() === ''){
            return
        }
        if (!user) {
            throw new Error('You must be logged in')
        }

        const prompt = {
            content: newQuestion,
            type: "Text",
            author: {
                name: user.name,
                avatar: user.avatar
            },
        };

        // Safe prompt on firebase
        const db = database;
        const questionRef = ref(db, `rooms/${roomId}/prompts`);
        const newQuestRef = push(questionRef);
        await set (newQuestRef, prompt)

        setNewQuestion('');
    }

    return(
        <div id="page-room">
            <header>
                <div className="content">
                    <Link to="/"><img src={logoImg} alt="SummAIze" /></Link>
                    <RoomCode code={roomId} />
                </div>
            </header>

            <main>
                <div className="room-title">
                    <h1>Room {title}</h1>
                    { prompts.length > 0 && <span>{prompts.length} prompts(s)</span>}
                </div>
                
                <div className="prompt-list">
                    <div className="prompt-container"> 
                        {prompts.map(prompt => {
                            return (
                                <Prompt 
                                    key={prompt.id}
                                    content={prompt.content}
                                    author={prompt.author}
                                    type={prompt.type}
                                    fileURL={prompt.fileURL}
                                ></Prompt>
                            )
                        })}
                    </div>
                </div>

                { prompts.length < 1 && (<MessageShare admin/>) }

                <form onSubmit={handleSendQuestion}>
                    <textarea 
                        placeholder='Write here...'
                        onChange={(event) => {setNewQuestion(event.target.value);}}
                        value={newQuestion}
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
                            <Button className="btn-icon" type="submit" onClick={handleAttachFile} disabled={!user}><img className='icon' src={iconAttached}/></Button>
                            <Button className="btn-icon" type="submit" onClick={handleAIGenerate} disabled={!user}><img className='icon' src={iconAI}/></Button>
                            <Button className="btn-icon" type="submit" disabled={!user}><img className='icon' src={iconSend} alt={"send"} /></Button>
                        </div>
                    </div>
                </form>

             </main>

            {isUploadModalOpen && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h2>Attach PDF File</h2>
                        
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

        </div>
    );
}
