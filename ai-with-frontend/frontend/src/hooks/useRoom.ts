// Hook that will retrieve prompts from the database, along with the room name.
import { useEffect, useState } from 'react';
import { database, ref, onValue, off} from '../services/firebase';
import { useAuth } from './useAuth';

type FirebasePrompts = Record<string, {
    author: {
        name: string;
        avatar: string;
    },
    content: string;
    type: 'Text' | 'PDF';
    fileURL?: string;
}>

type PromptType = {
    id: string,
    author: {
        name: string;
        avatar: string;
    },
    content: string;
    type: 'Text' | 'PDF';
    fileURL?: string;
    likeCount: number;
    likeId: string | undefined;
}

export function useRoom(roomId: string){
    const { user } = useAuth();
    const [ prompts, setPrompts ] = useState<PromptType[]>([]);
    const [ title, setTitle ] = useState<string>();

    useEffect(() => {
        const db = database;
        const roomRef = ref(db, `rooms/${roomId}`);

        onValue(roomRef, (room) => {
            const databaseRoom = room.val();
            const firebasePrompts: FirebasePrompts = databaseRoom.prompts ?? {};
            const parsedPrompts = Object.entries(firebasePrompts).map(([key, value]) => {
                
                const promptType = value.type ?? 'Text'; 
                const fileUrl = value.fileURL;
                
                return {
                    id: key,
                    content: value.content,
                    author: value.author,
                    type: promptType,
                    fileURL: fileUrl,
                } as PromptType;
            })

            setTitle(databaseRoom.title)
            setPrompts(parsedPrompts);
        })

        return () => {
            off(roomRef, 'value')
        }

    }, [roomId, user?.id])

    return { prompts, title }

}