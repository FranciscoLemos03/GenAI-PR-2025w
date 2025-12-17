import { useNavigate, Link } from 'react-router-dom'
import { FormEvent, useState } from 'react'

import illustrationImg from '../assets/images/illustration.svg'
import logoImg from '../assets/images/logo.svg'

import '../styles/auth.scss'
import { Button } from '../components/Button'
import { useAuth } from '../hooks/useAuth'
import { database, set, ref, push } from '../services/firebase';

export function NewRoom(){
    
  const { user } = useAuth();
  const [newRoom, setNewRoom] = useState('');
  const navigate = useNavigate();

  async function handleCreateRoom(event: FormEvent){
      event.preventDefault();
      
      if (newRoom.trim() === '') {
          return
      }
      
      const db = database;
      const roomRef = ref(db, 'rooms');
      
      const newPostRef = push(roomRef);
      await set (newPostRef, {
          title: newRoom,
          authorId: user?.id
      })

      navigate(`/admin/rooms/${newPostRef.key}`);
  }

    return(
    <div id='page-auth'>
      <aside>
        <img
          src={illustrationImg}
          alt="Illustration symbolizing questions and answers"
        />
        <strong>Search. Summarize. <br/> Understand.</strong>
        <p>Make your investigations more robust, and never lose information again.</p>
      </aside>
      <main>
        <div className='main-content'>
          <img src={logoImg} alt="SummAIze" />
          <h2>Create a new room</h2>
          <form onSubmit={handleCreateRoom}>
            <input
              type="text"
              placeholder="Room name"
              onChange={event => setNewRoom(event.target.value)}
              value={newRoom}
            />
            <Button type="submit">
              Create Room
            </Button>
          </form>
          <p>
            Would you like to join an existing room? <Link to="/">Click here</Link>
          </p>
        </div>
      </main>
    </div>
    )
}