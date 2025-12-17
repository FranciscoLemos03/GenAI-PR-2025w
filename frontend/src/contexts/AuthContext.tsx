// imports do firebase
import { auth } from '../services/firebase';
import { GoogleAuthProvider, signInWithPopup } from 'firebase/auth';
// imports do react
import { createContext, ReactNode, useState, useEffect } from 'react';

// User typing
type User = {
    id: string,
    name: string,
    avatar: string,
  }
  
  // AuthContextType typing
  type AuthContextType = {
    user: User | undefined,
    signInWithGoogle: () => Promise<void>,
  }

  type AuthContextProviderProps = {
    children: ReactNode,
  }

export const AuthContext = createContext({} as AuthContextType);;

export function AuthContextProvider(props: AuthContextProviderProps){

  const [user, setUser] = useState<User>();

  // Function that checks whether the user is logged in
  useEffect(() => {
      const unsubscribe = auth.onAuthStateChanged(user => {
        if (user) {
          const { displayName, photoURL, uid } = user;

          if (!displayName ||!photoURL) {
              throw new Error('Missing information from Google account'); 
          }

          setUser({ 
            id: uid,
            name: displayName,
            avatar: photoURL
          });
        }
      })

      return () => {
        unsubscribe();
      }

    },
  []);

  // Function to log in with Google account; if the user does not have a name or photo, an error occurs
  async function signInWithGoogle() {

    const provider = new GoogleAuthProvider();
    const result = await signInWithPopup(auth, provider);

   
      if (result.user) {
        const { displayName, photoURL, uid } = result.user;

        if (!displayName ||!photoURL) {
            throw new Error('Missing information from Google account'); 
        }

        setUser({ 
          id: uid,
          name: displayName,
          avatar: photoURL
        });
      }
  }  
  
    return (
        <AuthContext.Provider value={{ user, signInWithGoogle }}>
          {props.children}
        </AuthContext.Provider>
    );
}